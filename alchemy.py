import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

engine = sqlalchemy.create_engine('sqlite:///blog.db')
metadata = sqlalchemy.MetaData()

# Создание структуры 1 способ
post_table = sqlalchemy.Table('posts', metadata,
                              sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                              sqlalchemy.Column('user_id', sqlalchemy.Integer, nullable=False),
                              sqlalchemy.Column('title', sqlalchemy.Integer, nullable=False),
                              sqlalchemy.Column('text', sqlalchemy.String(16), nullable=False),
                              sqlalchemy.Column('is_published', sqlalchemy.Boolean, default=False),

                              )
# Создание структуры 2 способ через класс
Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String(16), nullable=False)
    is_published = sqlalchemy.Column(sqlalchemy.Boolean, default=False)


if __name__ == '__main__':
    # metadata.create_all(engine)
    Base.metadata.create_all(engine)
