"""empty message

Revision ID: 63523d82bb25
Revises: b506a7852b7d
Create Date: 2024-11-12 06:58:04.510341

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63523d82bb25'
down_revision = 'b506a7852b7d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('code_challenges')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('code_challenges',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('flag', sa.VARCHAR(), nullable=False),
    sa.Column('vuln_code', sa.VARCHAR(), nullable=False),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
