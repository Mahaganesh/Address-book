"""Added initial table

Revision ID: 19330d5a83e4
Revises: 
Create Date: 2022-04-30 00:06:44.746649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19330d5a83e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('uuid', sa.String(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('firstname', sa.String(length=100), nullable=True),
    sa.Column('lastname', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=200), nullable=True),
    sa.Column('password', sa.LargeBinary(), nullable=True),
    sa.Column('mobile_no', sa.String(length=20), nullable=True),
    sa.Column('probile_url', sa.String(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.uuid'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['users.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
