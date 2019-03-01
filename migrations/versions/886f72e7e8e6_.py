"""empty message

Revision ID: 886f72e7e8e6
Revises: 
Create Date: 2019-02-21 11:39:42.987189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '886f72e7e8e6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('webchat', sa.Column('color', sa.String(length=50), nullable=True))
    op.add_column('webchat', sa.Column('conduct', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('webchat', 'conduct')
    op.drop_column('webchat', 'color')
    # ### end Alembic commands ###