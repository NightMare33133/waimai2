"""empty message

Revision ID: 4cf9f6b084f7
Revises: fcaa6399d941
Create Date: 2022-02-23 19:06:53.422567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4cf9f6b084f7'
down_revision = 'fcaa6399d941'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('xiadan', sa.Column('telephone_number', sa.String(length=200), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('xiadan', 'telephone_number')
    # ### end Alembic commands ###
