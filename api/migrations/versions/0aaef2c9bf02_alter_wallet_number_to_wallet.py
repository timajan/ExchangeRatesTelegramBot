"""Alter wallet_number to wallet

Revision ID: 0aaef2c9bf02
Revises: b3d402749ac2
Create Date: 2024-06-03 09:11:48.458574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0aaef2c9bf02'
down_revision = 'b3d402749ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('wallet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('number', sa.Integer(), nullable=True))
        batch_op.drop_constraint('wallet_wallet_number_key', type_='unique')
        batch_op.create_unique_constraint(None, ['number'])
        batch_op.drop_column('wallet_number')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('wallet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('wallet_number', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_unique_constraint('wallet_wallet_number_key', ['wallet_number'])
        batch_op.drop_column('number')

    # ### end Alembic commands ###
