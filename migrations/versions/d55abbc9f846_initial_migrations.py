"""Initial Migrations

Revision ID: d55abbc9f846
Revises: 
Create Date: 2025-01-08 19:21:20.080839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd55abbc9f846'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('size', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('target_user', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('type', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('image', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('details', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('colour', sa.String(length=50), nullable=False))
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=150),
               existing_nullable=False)
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.Text(),
               nullable=True)
        batch_op.drop_column('rating')
        batch_op.drop_column('ratting')
        batch_op.drop_column('updated_at')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('updated_at', sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('ratting', sa.VARCHAR(length=100), nullable=True))
        batch_op.add_column(sa.Column('rating', sa.FLOAT(), nullable=True))
        batch_op.alter_column('description',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=255),
               nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.String(length=150),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.drop_column('colour')
        batch_op.drop_column('details')
        batch_op.drop_column('image')
        batch_op.drop_column('type')
        batch_op.drop_column('target_user')
        batch_op.drop_column('size')

    # ### end Alembic commands ###