"""renamed followers-only

Revision ID: fa271cc0ded9
Revises: 4df0a061def2
Create Date: 2024-03-20 12:36:08.875582

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fa271cc0ded9'
down_revision = '4df0a061def2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('users_only', sa.Boolean(), nullable=True))
        batch_op.drop_column('followers_only')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('followers_only', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
        batch_op.drop_column('users_only')

    # ### end Alembic commands ###
