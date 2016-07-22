"""empty message

Revision ID: 2e6bd753576
Revises: 155aff379cc5
Create Date: 2016-05-05 16:31:08.378902

"""

# revision identifiers, used by Alembic.
revision = '2e6bd753576'
down_revision = '155aff379cc5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'published')
    ### end Alembic commands ###