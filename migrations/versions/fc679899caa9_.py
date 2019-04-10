"""empty message

Revision ID: fc679899caa9
Revises: 7961ef6d4c3f
Create Date: 2019-04-03 16:04:40.676734

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fc679899caa9'
down_revision = '7961ef6d4c3f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bottom_wx', sa.Column('column', sa.String(length=50), nullable=True, comment='栏目'))
    op.add_column('bottom_wx', sa.Column('content', sa.String(length=200), nullable=True, comment='内容'))
    op.alter_column('bottom_wx', 'doger',
               existing_type=mysql.VARCHAR(length=100),
               comment='训犬师',
               existing_nullable=True)
    op.alter_column('bottom_wx', 'wx',
               existing_type=mysql.VARCHAR(length=100),
               comment='微信号',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('bottom_wx', 'wx',
               existing_type=mysql.VARCHAR(length=100),
               comment=None,
               existing_comment='微信号',
               existing_nullable=True)
    op.alter_column('bottom_wx', 'doger',
               existing_type=mysql.VARCHAR(length=100),
               comment=None,
               existing_comment='训犬师',
               existing_nullable=True)
    op.drop_column('bottom_wx', 'content')
    op.drop_column('bottom_wx', 'column')
    # ### end Alembic commands ###