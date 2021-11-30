"""add project and entry

Revision ID: e42c1d77a566
Revises: 32d068cc965e
Create Date: 2021-11-22 19:02:29.878181

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utc


# revision identifiers, used by Alembic.
revision = 'e42c1d77a566'
down_revision = '32d068cc965e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True), nullable=False),
    sa.Column('status', sa.String(length=32), nullable=True),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('creation_date', sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True), nullable=False),
    sa.Column('creation_user_id', sa.Integer(), nullable=False),
    sa.Column('last_update_date', sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True), nullable=False),
    sa.Column('last_update_user_id', sa.Integer(), nullable=False),
    sa.Column('extra', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['creation_user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['last_update_user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('entries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True), nullable=False),
    sa.Column('type', sa.String(length=16), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('creation_date', sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True), nullable=False),
    sa.Column('creation_user_id', sa.Integer(), nullable=False),
    sa.Column('last_update_date', sqlalchemy_utc.sqltypes.UtcDateTime(timezone=True), nullable=False),
    sa.Column('last_update_user_id', sa.Integer(), nullable=False),
    sa.Column('extra', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['creation_user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['last_update_user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entries')
    op.drop_table('projects')
    # ### end Alembic commands ###
