"""empty message

Revision ID: b594e8996f30
Revises: 238d85623c61
Create Date: 2023-10-04 18:22:53.039716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b594e8996f30'
down_revision = '238d85623c61'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tokens_blocklist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('tokens_blocklist', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_tokens_blocklist_jti'), ['jti'], unique=False)

    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)

    with op.batch_alter_table('tokens_blocklist', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_tokens_blocklist_jti'))

    op.drop_table('tokens_blocklist')
    # ### end Alembic commands ###