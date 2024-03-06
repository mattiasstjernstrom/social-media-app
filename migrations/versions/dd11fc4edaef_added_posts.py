"""added posts

Revision ID: dd11fc4edaef
Revises: 3462af51bd90
Create Date: 2024-03-06 10:23:13.182217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd11fc4edaef'
down_revision = '3462af51bd90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('splash_url', sa.String(length=100), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('date_edited', sa.DateTime(), nullable=True),
    sa.Column('draft', sa.Boolean(), nullable=True),
    sa.Column('friends_only', sa.Boolean(), nullable=True),
    sa.Column('followers_only', sa.Boolean(), nullable=True),
    sa.Column('likes', sa.Integer(), nullable=True),
    sa.Column('shares', sa.Integer(), nullable=True),
    sa.Column('comments', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_post_comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('date_commented', sa.DateTime(), nullable=False),
    sa.Column('date_edited', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['user_posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_post_likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('date_liked', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['user_posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_post_shares',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('date_shared', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['user_posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_post_shares')
    op.drop_table('user_post_likes')
    op.drop_table('user_post_comments')
    op.drop_table('user_posts')
    # ### end Alembic commands ###
