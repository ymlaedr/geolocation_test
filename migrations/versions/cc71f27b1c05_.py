"""empty message

Revision ID: cc71f27b1c05
Revises: 
Create Date: 2023-02-12 15:13:16.343841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc71f27b1c05'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('geolocation_recorder',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_agent', sa.String(), nullable=False),
    sa.Column('cookie_id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('geolocation_coordinates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('geolocation_recorder_id', sa.Integer(), nullable=True),
    sa.Column('latitude', sa.Double(), nullable=True),
    sa.Column('longitude', sa.Double(), nullable=True),
    sa.Column('altitude', sa.Double(), nullable=True),
    sa.Column('accuracy', sa.Double(), nullable=True),
    sa.Column('altitudeAccuracy', sa.Double(), nullable=True),
    sa.Column('heading', sa.Double(), nullable=True),
    sa.Column('meter_per_second', sa.Double(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['geolocation_recorder_id'], ['geolocation_recorder.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('geolocation_coordinates')
    op.drop_table('geolocation_recorder')
    # ### end Alembic commands ###
