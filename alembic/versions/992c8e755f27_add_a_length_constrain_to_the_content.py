"""add a length constrain to the content

Revision ID: 992c8e755f27
Revises: b165819dd57b
Create Date: 2024-12-18 14:15:16.963898

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '992c8e755f27'
down_revision: Union[str, None] = 'b165819dd57b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("posts", "content", type_=sa.String(length=200))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("posts", "content",type_=sa.String())
    pass
    # ### end Alembic commands ###
