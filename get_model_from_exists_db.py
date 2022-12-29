import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///blog.db')
metadata = sqlalchemy.MetaData()

# Подтягшивание модели из суцествующей БД
if __name__ == '__main__':
    posts_table = sqlalchemy.Table('posts', metadata, autoload=True, autoload_with=engine)
    print([c.name for c in posts_table.columns])
    # ['id', 'user_id', 'title', 'text', 'is_published']
