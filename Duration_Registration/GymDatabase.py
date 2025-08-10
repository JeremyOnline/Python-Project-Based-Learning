import sqlite3
import os
from datetime import datetime

class GymDatabase:
    def __init__(self, db_path='gym_database.db'):
        self.db_path = os.path.join(os.path.dirname(__file__), db_path)
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create members table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                phone TEXT,
                join_date DATE DEFAULT CURRENT_DATE
            )
        ''')
        
        # Create gym_sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gym_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER,
                check_in_time DATETIME,
                check_out_time DATETIME,
                duration_minutes INTEGER,
                FOREIGN KEY (member_id) REFERENCES members (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_member(self, name, email=None, phone=None):
        """Add new member to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO members (name, email, phone)
                VALUES (?, ?, ?)
            ''', (name, email, phone))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def get_all_members(self):
        """Get all members"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM members ORDER BY name')
        members = cursor.fetchall()
        
        conn.close()
        return members
    
    def find_member_by_name(self, name):
        """Find member by name"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM members WHERE name = ?', (name,))
        member = cursor.fetchone()
        
        conn.close()
        return member
    
    def record_check_in(self, member_name):
        """Record member check-in"""
        member = self.find_member_by_name(member_name)
        if not member:
            # Auto-add new member if not exists
            member_id = self.add_member(member_name)
            if not member_id:
                return False
        else:
            member_id = member[0]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        check_in_time = datetime.now()
        cursor.execute('''
            INSERT INTO gym_sessions (member_id, check_in_time)
            VALUES (?, ?)
        ''', (member_id, check_in_time))
        
        conn.commit()
        session_id = cursor.lastrowid
        conn.close()
        
        return session_id
    
    def record_check_out(self, member_name):
        """Record member check-out and calculate duration"""
        member = self.find_member_by_name(member_name)
        if not member:
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Find active session (check_out_time is NULL)
        cursor.execute('''
            SELECT id, check_in_time FROM gym_sessions 
            WHERE member_id = ? AND check_out_time IS NULL
            ORDER BY check_in_time DESC LIMIT 1
        ''', (member[0],))
        
        session = cursor.fetchone()
        if not session:
            conn.close()
            return False
        
        session_id = session[0]
        check_in_time = datetime.fromisoformat(session[1])
        check_out_time = datetime.now()
        
        # Calculate duration in minutes
        duration = int((check_out_time - check_in_time).total_seconds() / 60)
        
        cursor.execute('''
            UPDATE gym_sessions 
            SET check_out_time = ?, duration_minutes = ?
            WHERE id = ?
        ''', (check_out_time, duration, session_id))
        
        conn.commit()
        conn.close()
        
        return duration
    
    def get_member_sessions(self, member_name):
        """Get all sessions for a member"""
        member = self.find_member_by_name(member_name)
        if not member:
            return []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT check_in_time, check_out_time, duration_minutes
            FROM gym_sessions
            WHERE member_id = ?
            ORDER BY check_in_time DESC
        ''', (member[0],))
        
        sessions = cursor.fetchall()
        conn.close()
        
        return sessions
    
    def get_active_sessions(self):
        """Get all active sessions (members currently in gym)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.name, s.check_in_time
            FROM members m
            JOIN gym_sessions s ON m.id = s.member_id
            WHERE s.check_out_time IS NULL
            ORDER BY s.check_in_time
        ''')
        
        active_sessions = cursor.fetchall()
        conn.close()
        
        return active_sessions
    
    def get_member_stats(self, member_name):
        """Get member statistics"""
        member = self.find_member_by_name(member_name)
        if not member:
            return None
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total visits
        cursor.execute('''
            SELECT COUNT(*) FROM gym_sessions
            WHERE member_id = ?
        ''', (member[0],))
        total_visits = cursor.fetchone()[0]
        
        # Total duration
        cursor.execute('''
            SELECT SUM(duration_minutes) FROM gym_sessions
            WHERE member_id = ? AND duration_minutes IS NOT NULL
        ''', (member[0],))
        total_duration = cursor.fetchone()[0] or 0
        
        # Last visit
        cursor.execute('''
            SELECT MAX(check_in_time) FROM gym_sessions
            WHERE member_id = ?
        ''', (member[0],))
        last_visit = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_visits': total_visits,
            'total_duration_minutes': total_duration,
            'last_visit': last_visit
        }
