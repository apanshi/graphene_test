from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test:test@192.168.1.2:3306/study?charset=utf8'

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    name = Column(String(132))

    def __str__(self):
        return f"Book[id:{self.id}, name:{self.name}]"


class BookQuery(SQLAlchemyObjectType):
    class Meta:
        model = Book

class Query(graphene.ObjectType):
    books = graphene.List(BookQuery)
    book = BookQuery
    print("eeeccc")

    def resolve_books(self, info):
        print("aaa")
        print(info)
        query = BookQuery.get_query(info)  # SQLAlchemy query
        return query.all()

    def resolve_book(self, info):
        print("ccc")
        print(info)
        query = BookQuery.get_query(info)  # SQLAlchemy query
        print(query.filter(Book.id == 2))
        return query.filter(Book.id == 2).first()

schema = graphene.Schema(query = Query)


query = '''
{books {
  id
  name
}
book
}
'''.strip()

query = '''
book {
  id
  name
}
'''.strip()


result = schema.execute(query, context_value={'session': session})
print("bbbb")
print(result.data)
