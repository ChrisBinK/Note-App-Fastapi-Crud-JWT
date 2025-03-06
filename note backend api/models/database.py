from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from environs import env
env.read_env()

postgresql_url = URL.create(
    drivername= env('DRIVER_NAME'),
    username=env('USERNAME'),
    password=env('PASSWORD'),
    host= env('HOST'),
    database=env('DB_NAME'),
    port=env('PORT')
)

engine = create_engine(env('DB_URL'))
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
#metadata = Base.metadata
