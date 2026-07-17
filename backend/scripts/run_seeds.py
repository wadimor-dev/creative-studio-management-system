from seed_roles import seed_roles
from seed_divisions import seed_divisions
from seed_locations import seed_locations
from seed_work_categories import seed_work_categories
from seed_admin import seed_admin

if __name__ == "__main__":
    seed_roles()
    seed_divisions()
    seed_locations()
    seed_work_categories()
    seed_admin()

    print("================================")
    print("All seeds executed successfully.")
    print("================================")