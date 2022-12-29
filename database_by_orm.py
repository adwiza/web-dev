import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

engine = sqlalchemy.create_engine('sqlite:///db1.db')
metadata = sqlalchemy.MetaData()

Base = declarative_base()


class Post(Base):

    __tablename__ = 'posts'

    id = sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column('user_id', sqlalchemy.Integer, nullable=False)
    title = sqlalchemy.Column('title', sqlalchemy.String(16), nullable=False)
    text = sqlalchemy.Column('text', sqlalchemy.Text, nullable=False)
    is_published = sqlalchemy.Column('is_published', sqlalchemy.Boolean, nullable=False)


if __name__ == '__main__':

    Base.metadata.create_all(engine)
