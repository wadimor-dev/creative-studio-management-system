"""007f add notes column to showroom_movement_types + seed descriptions

Revision ID: 007f7a607184
Revises: 006f6a607183
Create Date: 2026-07-21 15:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '007f7a607184'
down_revision: Union[str, Sequence[str], None] = '006f6a607183'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NOTES = {
    "ADJUSTMENT": "Koreksi stok hasil stock opname atau kesalahan pencatatan.",
    "BORROW": "Barang dipinjam dan dikembalikan.",
    "HANDOVER": "Barang masuk ke showroom dari inventory / produksi.",
    "MAINTENANCE_OUT": "Barang keluar untuk perawatan dan kembali setelah selesai.",
    "MAINTENANCE_RETURN": "Barang kembali setelah selesai perawatan.",
    "RELEASE": "Barang keluar permanen tanpa harapan kembali (hadiah, sampel gratis, sponsorship, dll.).",
    "RELEASE_REJECT": "Barang release ditolak / dibatalkan.",
    "RESTOCK": "Penambahan stok baru (produksi, pembelian, hibah).",
    "RETIRED": "Aset dinonaktifkan dari operasional.",
    "RETURN": "Barang dikembalikan setelah dipinjam.",
    "SCRAP": "Barang dimusnahkan atau dibuang karena rusak berat.",
    "SHOWROOM_IN": "Barang masuk ke showroom dari lokasi lain.",
    "SHOWROOM_OUT": "Barang keluar dari showroom ke lokasi di luar jaringan showroom atau ke gudang.",
    "TRANSFER": "Barang dipindahkan antar lokasi showroom.",
    "TRANSFER_IN": "Barang diterima dari lokasi ERP lain (antar cabang/antar showroom).",
    "TRANSFER_OUT": "Barang dikirim ke lokasi ERP lain (antar cabang/antar showroom).",
}


def upgrade() -> None:
    conn = op.get_bind()
    r = conn.execute(sa.text(
        "SELECT COUNT(*) FROM information_schema.columns "
        "WHERE table_schema = DATABASE() AND table_name = 'showroom_movement_types' "
        "AND column_name = 'notes'"
    ))
    if r.scalar() == 0:
        op.add_column('showroom_movement_types', sa.Column('notes', sa.Text(), nullable=True))

    for code, notes in NOTES.items():
        op.execute(
            sa.text("UPDATE showroom_movement_types SET notes = :notes WHERE code = :code AND notes IS NULL")
            .bindparams(code=code, notes=notes)
        )


def downgrade() -> None:
    conn = op.get_bind()
    r = conn.execute(sa.text(
        "SELECT COUNT(*) FROM information_schema.columns "
        "WHERE table_schema = DATABASE() AND table_name = 'showroom_movement_types' "
        "AND column_name = 'notes'"
    ))
    if r.scalar() > 0:
        op.drop_column('showroom_movement_types', 'notes')
