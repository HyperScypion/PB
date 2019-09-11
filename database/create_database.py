from sqlalchemy import MetaData, create_engine, Table, Column, Integer, String, ForeignKey, Float, event
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import DDL


Base = declarative_base()
engine = create_engine('sqlite:///data.db', echo=True)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    salt = Column(String, nullable=False)
    admin = Column(Integer, default=0, nullable=False)


class Car(Base):
     __tablename__ = 'car'
     id = Column(Integer, primary_key=True, autoincrement=True)
     carMake = Column(String, nullable=False)
     carModel = Column(String, nullable=True)


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    productName = Column(String)
    productPrice = Column(Float)
    productMake = Column(String)


class Orderes(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey('user.id'))


class Link(Base):
    __tablename__ = 'link'
    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id', primart_key=True))




# event.listen(
#     User.__table__, 'before_insert',
#    DDL("""
#    """)
# )

Base.metadata.create_all(engine)
