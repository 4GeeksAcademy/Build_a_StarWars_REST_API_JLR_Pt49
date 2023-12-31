"""empty message

Revision ID: cf660df507e1
Revises: 2e98c76e4303
Create Date: 2023-12-15 10:14:54.240631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf660df507e1'
down_revision = '2e98c76e4303'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('type_of_terrain', sa.String(length=120), nullable=False),
    sa.Column('population', sa.String(length=120), nullable=False),
    sa.Column('diameter', sa.String(length=120), nullable=False),
    sa.Column('climate', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.drop_table('planet')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('type_of_terrain', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('population', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('diameter', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('climate', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='planet_pkey'),
    sa.UniqueConstraint('name', name='planet_name_key')
    )
    op.drop_table('planets')
    # ### end Alembic commands ###
