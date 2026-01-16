from alembic import op
import sqlalchemy as sa
from datetime import datetime


revision = "20260116_create_currency_prices"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "currency_prices",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("ticker", sa.String(length=10), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("timestamp", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_currency_prices_ticker", "currency_prices", ["ticker"])
    op.create_index("ix_currency_prices_timestamp", "currency_prices", ["timestamp"])
    op.create_index("idx_ticker_timestamp", "currency_prices", ["ticker", "timestamp"])


def downgrade() -> None:
    op.drop_index("idx_ticker_timestamp", table_name="currency_prices")
    op.drop_index("ix_currency_prices_timestamp", table_name="currency_prices")
    op.drop_index("ix_currency_prices_ticker", table_name="currency_prices")
    op.drop_table("currency_prices")
