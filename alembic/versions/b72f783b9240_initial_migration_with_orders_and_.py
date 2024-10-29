"""Initial migration with orders and transactions

Revision ID: b72f783b9240
Revises: 85558d5168cb
Create Date: 2024-10-29 12:23:02.003899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b72f783b9240'
down_revision: Union[str, None] = '85558d5168cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('sign', sa.Enum('positive', 'negative', name='sign'), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('transaction_number', sa.String(), nullable=True),
    sa.Column('transaction_type', sa.Enum('deposit', 'withdrawal', name='transactiontype'), nullable=False),
    sa.Column('status', sa.Enum('pending', 'completed', 'failed', name='transactionstatus'), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('transaction_number')
    )
    op.create_index(op.f('ix_transactions_id'), 'transactions', ['id'], unique=False)
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product', sa.Integer(), nullable=False),
    sa.Column('deadline', sa.DateTime(), nullable=False),
    sa.Column('for_final_date', sa.DateTime(), nullable=True),
    sa.Column('language', sa.Enum('english_us', 'english_uk', 'spanish_es', 'french_fr', name='language'), nullable=True),
    sa.Column('level', sa.Enum('high_school', 'college', 'bachelors', 'masters', 'doctorate', name='academic'), nullable=False),
    sa.Column('service', sa.Enum('writing', 'rewriting', 'editing', 'proofreading', 'problem_solving', 'calculations', name='service'), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('space', sa.Integer(), nullable=False),
    sa.Column('words_count', sa.Integer(), nullable=False),
    sa.Column('size_type', sa.String(), nullable=False),
    sa.Column('topic', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('subject', sa.String(), nullable=False),
    sa.Column('number_of_sources', sa.Integer(), nullable=False),
    sa.Column('style', sa.Enum('APA_6th', 'APA_7th', 'ASA', 'Bluebook', 'Chicago_Turabian', 'Harvard', 'IEEE', 'MLA', 'Other', 'Not_applicable', name='citationstyle'), nullable=False),
    sa.Column('is_private', sa.Boolean(), nullable=True),
    sa.Column('promocode', sa.String(), nullable=True),
    sa.Column('client_id', sa.String(), nullable=False),
    sa.Column('status', sa.Enum('draft', 'open', 'closed', name='orderstatus'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_orders_id'), 'orders', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_orders_id'), table_name='orders')
    op.drop_table('orders')
    op.drop_index(op.f('ix_transactions_id'), table_name='transactions')
    op.drop_table('transactions')
    # ### end Alembic commands ###
