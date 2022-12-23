"""Add words db

Revision ID: 4751138fde4c
Revises: 9578d24725a9
Create Date: 2022-12-17 18:59:12.291362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4751138fde4c'
down_revision = '9578d24725a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('words',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=56), nullable=False),
    sa.Column('words', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('category')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('words')
    # ### end Alembic commands ###
