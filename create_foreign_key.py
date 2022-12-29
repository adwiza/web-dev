import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, session

engine = sqlalchemy.create_engine('sqlite:///blog.db')
metadata = sqlalchemy.MetaData()

# Создание структуры 2 способ через класс
Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey('users.id'), nullable=False)
    title = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String(16), nullable=False)
    is_published = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    user = relationship('User', back_populates='posts')


class User(Base):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_name = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)

    posts = relationship('Post', back_populates='user', lazy='joined')


# Использование  ForeignKey

post = session.query(Post).first()  # в этот момент делается select from posts join users (если lazy='joined')
print(post.user.username)  # есть доступ до объекта user

if __name__ == '__main__':
    Base.metadata.create_all(engine)


