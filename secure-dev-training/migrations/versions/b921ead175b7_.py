"""empty message

Revision ID: b921ead175b7
Revises: 6d8fc1969095
Create Date: 2024-07-09 13:06:52.064437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b921ead175b7'
down_revision = '6d8fc1969095'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_challenge_completions')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_challenge_completions',
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('challenge_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['challenge_id'], ['challenge.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'challenge_id')
    )
    # ### end Alembic commands ###