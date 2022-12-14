"""el atributo iba en persona no en contacto

Revision ID: 98643a6f9406
Revises: 593851e3b0a9
Create Date: 2022-09-13 15:52:10.321384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98643a6f9406'
down_revision = '593851e3b0a9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contactos', 'estaOculto')
    op.add_column('personas', sa.Column('estaOculto', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('personas', 'estaOculto')
    op.add_column('contactos', sa.Column('estaOculto', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
