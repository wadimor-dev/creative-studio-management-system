class RoleType:
    """Role constants - stored in UPPERCASE for consistency"""
    ADMIN = "ADMIN"
    STAFF = "STAFF"
    MANAGER = "MANAGER"
    CREATIVE = "CREATIVE"
    
    # For database lookup (these are display names)
    ROLES_MAP = {
        "ADMIN": "Admin",
        "STAFF": "Staff", 
        "MANAGER": "Manager",
        "CREATIVE": "Creative"
    }
