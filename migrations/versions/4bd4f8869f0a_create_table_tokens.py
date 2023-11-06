"""create table tokens

Revision ID: 4bd4f8869f0a
Revises: 5bf7f22a2210
Create Date: 2023-11-06 13:54:30.316742

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4bd4f8869f0a'
down_revision: Union[str, None] = '5bf7f22a2210'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
