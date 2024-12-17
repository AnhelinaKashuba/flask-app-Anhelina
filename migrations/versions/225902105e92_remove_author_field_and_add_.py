from alembic import op
import sqlalchemy as sa

def upgrade():
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.create_foreign_key(
            'fk_posts_user_id',  # Ім'я обмеження
            'users',             # Таблиця для зовнішнього ключа
            ['user_id'],         # Поле у таблиці posts
            ['id']               # Поле у таблиці users
        )

def downgrade():
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_constraint('fk_posts_user_id', type_='foreignkey')
