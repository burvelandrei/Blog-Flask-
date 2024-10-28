from sqlalchemy import Table, Column, Integer, VARCHAR, ForeignKey, String
from sqlalchemy.orm import relationship
from db.Base_Model import BaseModel
from db.db_connect import engine


# Определям модель таблицы publication
class Publication(BaseModel):
    __tablename__ = "publication"

    title = Column(VARCHAR(70))
    text_publication = Column(String)
    comments = relationship("Comment", backref="publication")



# Определям модель таблицы comment
class Comment(BaseModel):
    __tablename__ = "comment"

    text_comment = Column(Integer)
    text_publication_id = Column(Integer, ForeignKey(Publication.id, ondelete="CASCADE"))


def create_tables():
    """
    Функция для создания всех таблиц.
    """
    BaseModel.metadata.create_all(engine)
    engine.echo = True