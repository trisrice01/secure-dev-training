"""empty message

Revision ID: ce8a01891dc4
Revises: 
Create Date: 2024-06-23 21:19:20.579373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce8a01891dc4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('rdp_server',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip_addr', sa.String(length=64), nullable=False),
    sa.Column('is_taken', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('rdp_server', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_rdp_server_ip_addr'), ['ip_addr'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rdp_server', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_rdp_server_ip_addr'))

    op.drop_table('rdp_server')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))

    op.drop_table('user')
    # ### end Alembic commands ###
