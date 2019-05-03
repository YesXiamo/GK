#!/usr/bin/env
# -*-coding:utf8;-*-
#__author__ = 'ぺ嫙嵂'

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from init import db_name

__engine = create_engine("sqlite:///{}.db".format(db_name))
DBSession = sessionmaker(bind=__engine, autocommit=False)
metadata = MetaData(__engine)


@contextmanager
def getSession():
    session = DBSession()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
