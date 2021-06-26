"""empty message

Revision ID: abdafdf57b0c
Revises: 6156df22f756
Create Date: 2021-06-24 19:12:25.488659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abdafdf57b0c'
down_revision = '6156df22f756'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('counselor', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_counselor_username'), ['username'])

    with op.batch_alter_table('respond', schema=None) as batch_op:
        batch_op.alter_column('user_foreignkey',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('respond', schema=None) as batch_op:
        batch_op.alter_column('user_foreignkey',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('counselor', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_counselor_username'), type_='unique')

    # ### end Alembic commands ###