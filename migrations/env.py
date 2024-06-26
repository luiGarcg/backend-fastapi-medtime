import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from decouple import config as decouple_config

# Adicione o caminho raiz do seu projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importe seus modelos SQLAlchemy após ajustar sys.path
from app.db.models import Base

# Configurações padrão do Alembic
config = context.config

# Configura a URL do SQLAlchemy usando a variável de ambiente DATABASE_URL
config.set_main_option('sqlalchemy.url', decouple_config('DATABASE_URL'))

# Configura o logging usando as configurações do arquivo .ini do Alembic
if config.config_file_name:
    fileConfig(config.config_file_name)

# Define os metadados-alvo para suporte ao 'autogenerate'
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Executa migrações no modo 'offline'.

    Este modo configura o contexto apenas com uma URL
    e não requer a criação de um Engine, embora um Engine
    seja aceitável aqui também. Ao pular a criação do Engine,
    não precisamos de um DBAPI disponível.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa migrações no modo 'online'.

    Neste cenário, precisamos criar um Engine
    e associar uma conexão ao contexto.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
