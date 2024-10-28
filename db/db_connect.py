from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.config_db import DB, load_config

# Загружаем параметры базы данных
config_db: DB = load_config()


# Создание движка для базы данных
engine = create_engine(
    f"""postgresql+psycopg2://{config_db.db_user}:{config_db.db_password}@{config_db.db_host}:{config_db.db_port}/{config_db.db_name}""",
    echo=True,
)

Session = sessionmaker(bind=engine)

def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()