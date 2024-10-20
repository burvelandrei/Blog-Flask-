from sqlalchemy import Table, Column, Integer, VARCHAR, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from db.db_connect import engine


# Базовый класс для всех моделей!! переписать через класс
Base = declarative_base()


# Определям модель таблицы author
class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(50), nullable=False)


# Определям модель таблицы text
class Text(Base):
    __tablename__ = "text"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
    author_id = Column(Integer, ForeignKey(Author.id))


# # Определям модель таблицы book
# class Book_orm(Base):
#     __tablename__ = "book"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     title = Column(VARCHAR(50), nullable=False)
#     publication_year = Column(Integer)
#     author_id = Column(Integer, ForeignKey(Author_orm.id, ondelete="CASCADE"))
#     genre_id = Column(Integer, ForeignKey(Genre_orm.id, ondelete="CASCADE"))



def create_tables_orm():
    """
    Функция для создания всех таблиц.
    """
    Base.metadata.create_all(engine)
    engine.echo = True