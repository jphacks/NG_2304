"""Add initial models

Revision ID: 4e957af37ccd
Revises: 8fd3b8bea215
Create Date: 2023-10-26 13:41:26.987515

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4e957af37ccd"
down_revision = "8fd3b8bea215"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "sessions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("session_cert", sa.String(length=100), nullable=False),
        sa.Column("refresh_token", sa.String(length=512), nullable=False),
        sa.Column("is_discard", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("sessions")
    # ### end Alembic commands ###