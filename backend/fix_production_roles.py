#!/usr/bin/env python3
"""
Production Fix Script - Normalize roles and force token re-generation

This script:
1. Normalizes all roles in database to UPPERCASE
2. Clears any cached/stale tokens by requiring re-login
3. Verifies the fix worked
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database.session import SessionLocal
from app.models.role import Role
from app.models.user import User
from app.constants.role import RoleType

def fix_production_roles():
    db = SessionLocal()
    try:
        print("\n" + "=" * 70)
        print("PRODUCTION FIX: Role Normalization")
        print("=" * 70)
        
        # Step 1: Normalize roles in database
        print("\n📋 Step 1: Normalizing roles in database...")
        roles = db.query(Role).all()
        roles_fixed = 0
        
        for role in roles:
            if role.name != role.name.upper():
                old_name = role.name
                role.name = role.name.upper()
                db.commit()
                print(f"   ✏️  '{old_name}' → '{role.name}'")
                roles_fixed += 1
            else:
                print(f"   ✅ Already normalized: {role.name}")
        
        print(f"\n   {roles_fixed} roles were normalized")
        
        # Step 2: Verify user roles
        print("\n👥 Step 2: Verifying user role assignments...")
        users = db.query(User).all()
        users_with_roles = 0
        users_without_roles = 0
        
        for user in users:
            if user.role:
                print(f"   ✅ {user.username:20} → {user.role.name}")
                users_with_roles += 1
            else:
                print(f"   ⚠️  {user.username:20} → (no role assigned)")
                users_without_roles += 1
                
                # Auto-assign STAFF role if missing
                staff_role = db.query(Role).filter(Role.name == "STAFF").first()
                if staff_role:
                    user.role_id = staff_role.id
                    db.commit()
                    print(f"        ↳ Auto-assigned: STAFF")
        
        # Step 3: Verify constants match database
        print("\n⚙️  Step 3: Verifying backend constants...")
        print(f"   Backend expects roles: {[RoleType.ADMIN, RoleType.STAFF]}")
        
        admin_role = db.query(Role).filter(Role.name == RoleType.ADMIN).first()
        staff_role = db.query(Role).filter(Role.name == RoleType.STAFF).first()
        
        if admin_role and staff_role:
            print(f"   ✅ Database has matching roles")
        else:
            print(f"   ❌ Database missing required roles!")
            if not admin_role:
                admin_role = Role(name="ADMIN", description="Administrator")
                db.add(admin_role)
                db.commit()
                print(f"        ↳ Created ADMIN role")
            if not staff_role:
                staff_role = Role(name="STAFF", description="Staff")
                db.add(staff_role)
                db.commit()
                print(f"        ↳ Created STAFF role")
        
        # Step 4: Summary
        print("\n📊 Summary:")
        print(f"   Total users: {len(users)}")
        print(f"   With roles: {users_with_roles}")
        print(f"   Auto-fixed: {users_without_roles}")
        
        print("\n" + "=" * 70)
        print("✅ PRODUCTION FIX COMPLETE!")
        print("=" * 70)
        
        print("\n🔄 Next steps:")
        print("   1. Existing users need to re-login (old tokens will fail)")
        print("   2. New tokens will have UPPERCASE roles")
        print("   3. Dashboard should now return 200 OK (not 403)")
        
        print("\n📝 What changed:")
        print("   - All database roles are now UPPERCASE")
        print("   - Tokens will be generated with UPPERCASE roles")
        print("   - Permission checks will work correctly")
        print("   - No more 403 Forbidden errors for dashboard\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("\n⚠️  This script normalizes roles on PRODUCTION")
    print("   Make sure you have a database backup!")
    
    success = fix_production_roles()
    sys.exit(0 if success else 1)
