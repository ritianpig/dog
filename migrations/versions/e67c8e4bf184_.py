"""empty message

Revision ID: e67c8e4bf184
Revises: 
Create Date: 2019-03-13 10:44:54.491754

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e67c8e4bf184'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('article_copy')
    op.add_column('ad2', sa.Column('remark', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ad2', 'remark')
    op.create_table('article_copy',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('article_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('article_name', mysql.VARCHAR(length=200), nullable=True),
    sa.Column('appid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('class_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('column_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('content', mysql.TEXT(), nullable=True),
    sa.Column('main_events', mysql.TEXT(), nullable=True),
    sa.Column('countcollect', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('countlike', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('create_date', mysql.DATETIME(), nullable=True),
    sa.Column('imageNum', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('is_audit', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('is_collect', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('is_like', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('url', mysql.VARCHAR(length=200), nullable=True),
    sa.Column('class_name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('column_name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('bigclass_name', mysql.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
