#!/usr/bin/env python3
"""
Migration: Normalize all roles to UPPERCASE

This script standardizes all role names in the database to UPPERCASE:
- Admin -> ADMIN
- Staff -> STAFF  
- Manager -> MANAGER
- Creative -> CREATIVE

This ensures consistency across the system for role-based access control.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.session import SessionLocal
from app.models.role import Role
from app.models.user import User

def normalize_roles():
    db = SessionLocal()
    try:
        print("=" * 60)
        print("Role Normalization Migration")
        print("=" * 60)
        
        # Get all roles
        roles = db.query(Role).all()
        
        print(f"\nFound {len(roles)} roles in database:")
        
        role_mapping = {}
        for role in roles:
            new_name = role.name.upper()
            role_mapping[role.id] = new_name
            
            if role.name != new_name:
                print(f"\n  ✏️  Normalizing: '{role.name}' → '{new_name}'")
                role.name = new_name
                db.commit()
            else:
                print(f"  ✅ Already normalized: '{role.name}'")
        
        # Show user role assignments
        print(f"\n\nUser Role Assignments:")
        users = db.query(User).all()
        for user in users:
            if user.role:
                print(f"  - {user.username:20} → {user.role.name}")
            else:
                print(f"  - {user.username:20} → (no role assigned)")
        
        print("\n" + "=" * 60)
        print("✅ Migration complete! All roles are now UPPERCASE")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = normalize_roles()
    sys.exit(0 if success else 1)
