"""Seed default showroom locations."""

from sqlalchemy.orm import Session
from app.models.showroom_location import ShowroomLocation


SHOWROOM_LOCATIONS = [
    {"code": "SHW-01", "name": "Showroom Utama", "type": "internal"},
    {"code": "SHW-02", "name": "Display Area", "type": "internal"},
    {"code": "SHW-03", "name": "Storage Showroom", "type": "internal"},
    {"code": "EXT-01", "name": "Gudang Eksternal", "type": "external"},
    {"code": "EXT-02", "name": "Cabang Bandung", "type": "external"},
]


def seed_showroom_locations(db: Session) -> None:
    """Insert default showroom locations if they don't exist."""
    existing_count = db.query(ShowroomLocation).count()
    if existing_count > 0:
        return

    for loc_data in SHOWROOM_LOCATIONS:
        location = ShowroomLocation(
            code=loc_data["code"],
            name=loc_data["name"],
            type=loc_data["type"],
        )
        db.add(location)

    db.commit()
    print(f"Seeded {len(SHOWROOM_LOCATIONS)} showroom locations")
