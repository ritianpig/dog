"""empty message

Revision ID: c9febd9adca5
Revises: 886f72e7e8e6
Create Date: 2019-03-01 10:20:33.036373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9febd9adca5'
down_revision = '886f72e7e8e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ad1', sa.Column('ad_str', sa.String(length=200), nullable=True))
    op.add_column('ad1', sa.Column('pic_url', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ad1', 'pic_url')
    op.drop_column('ad1', 'ad_str')
    # ### end Alembic commands ###
