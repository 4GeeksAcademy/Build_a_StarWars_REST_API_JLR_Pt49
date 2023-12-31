"""empty message

Revision ID: 60decc569468
Revises: 3b619b62340f
Create Date: 2023-12-13 20:26:14.778556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60decc569468'
down_revision = '3b619b62340f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nombre', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('planeta_natal', sa.String(length=80), nullable=False))
        batch_op.add_column(sa.Column('especie', sa.Boolean(), nullable=False))
        batch_op.drop_constraint('people_name_key', type_='unique')
        batch_op.create_unique_constraint(None, ['nombre'])
        batch_op.drop_column('otro_beta')
        batch_op.drop_column('name')
        batch_op.drop_column('age')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('age', sa.VARCHAR(length=80), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('otro_beta', sa.BOOLEAN(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_unique_constraint('people_name_key', ['name'])
        batch_op.drop_column('especie')
        batch_op.drop_column('planeta_natal')
        batch_op.drop_column('nombre')

    # ### end Alembic commands ###
