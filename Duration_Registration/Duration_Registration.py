import os
import sqlite3
import time
import datetime
from GymDatabase import GymDatabase

class GymRegistrationSystem:
    def __init__(self):
        self.db = GymDatabase()
    
    def register_new_member(self):
        """Register new member to database"""
        print("\n=== NEW MEMBER REGISTRATION ===")
        name = input("Enter member name: ").strip().capitalize()
        
        if not name:
            print("Name cannot be empty!")
            return None
        
        # Check if member already exists
        existing_member = self.db.find_member_by_name(name)
        if existing_member:
            print(f"Member '{name}' already exists!")
            return existing_member[0]
        
        email = input("Enter email (optional): ").strip()
        phone = input("Enter phone number (optional): ").strip()
        
        member_id = self.db.add_member(name, email if email else None, phone if phone else None)
        
        if member_id:
            print(f"✅ Member '{name}' registered successfully! Member ID: {member_id}")
            return member_id
        else:
            print("❌ Failed to register member!")
            return None
    
    def check_member_status(self, name):
        """Check member status and stats"""
        member = self.db.find_member_by_name(name)
        if not member:
            print(f"❌ Member '{name}' not found!")
            return False
        
        print(f"\n=== MEMBER PROFILE: {name} ===")
        print(f"Member ID: {member[0]}")
        print(f"Email: {member[2] or 'N/A'}")
        print(f"Phone: {member[3] or 'N/A'}")
        print(f"Join Date: {member[4]}")
        
        # Get member stats
        stats = self.db.get_member_stats(name)
        if stats:
            print(f"\n📊 STATISTICS:")
            print(f"Total Visits: {stats['total_visits']}")
            print(f"Total Duration: {stats['total_duration_minutes']} minutes")
            print(f"Last Visit: {stats['last_visit'] or 'Never'}")
        
        return True
    
    def member_check_in(self, name):
        """Record member check-in"""
        member = self.db.find_member_by_name(name)
        if not member:
            print(f"❌ Member '{name}' not found! Please register first.")
            return False
        
        session_id = self.db.record_check_in(name)
        if session_id:
            print(f"✅ {name} checked in successfully! Session ID: {session_id}")
            return True
        else:
            print("❌ Failed to check in!")
            return False
    
    def member_check_out(self, name):
        """Record member check-out"""
        duration = self.db.record_check_out(name)
        if duration:
            print(f"✅ {name} checked out successfully!")
            print(f"⏱️ Duration: {duration} minutes")
            return True
        else:
            print("❌ No active session found!")
            return False
    
    def list_all_members(self):
        """List all registered members"""
        members = self.db.get_all_members()
        if not members:
            print("❌ No members registered yet!")
            return
        
        print("\n=== ALL REGISTERED MEMBERS ===")
        print(f"{'ID':<5} {'Name':<20} {'Email':<25} {'Phone':<15} {'Join Date':<12}")
        print("-" * 80)
        
        for member in members:
            print(f"{member[0]:<5} {member[1]:<20} {member[2] or 'N/A':<25} {member[3] or 'N/A':<15} {member[4]:<12}")
    
    def get_active_sessions(self):
        """Show who is currently in the gym"""
        active_sessions = self.db.get_active_sessions()
        if not active_sessions:
            print("❌ No active sessions!")
            return
        
        print("\n=== CURRENTLY IN GYM ===")
        print(f"{'Name':<20} {'Check-in Time':<20}")
        print("-" * 40)
        
        for name, check_in in active_sessions:
            print(f"{name:<20} {check_in:<20}")
    
    def main_menu(self):
        """Main menu for gym registration system"""
        print("\n" + "="*50)
        print("🏋️ GYM REGISTRATION & TRACKING SYSTEM")
        print("="*50)
        
        while True:
            print("\n=== MAIN MENU ===")
            print("1. Register New Member")
            print("2. Member Check-in")
            print("3. Member Check-out")
            print("4. Check Member Profile")
            print("5. List All Members")
            print("6. View Active Sessions")
            print("7. Exit")
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                self.register_new_member()
            
            elif choice == "2":
                name = input("Enter member name: ").strip().capitalize()
                self.member_check_in(name)
            
            elif choice == "3":
                name = input("Enter member name: ").strip().capitalize()
                self.member_check_out(name)
            
            elif choice == "4":
                name = input("Enter member name: ").strip().capitalize()
                self.check_member_status(name)
            
            elif choice == "5":
                self.list_all_members()
            
            elif choice == "6":
                self.get_active_sessions()
            
            elif choice == "7":
                print("👋 Goodbye! Thank you for using our system.")
                break
            
            else:
                print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    system = GymRegistrationSystem()
    system.main_menu()
