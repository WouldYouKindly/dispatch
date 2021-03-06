"""Adds participant location column

Revision ID: fe8c213f2c54
Revises: 4691fc21e309
Create Date: 2020-03-18 15:02:02.866154

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fe8c213f2c54"
down_revision = "4691fc21e309"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("participant", sa.Column("location", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("participant", "location")
    # ### end Alembic commands ###
