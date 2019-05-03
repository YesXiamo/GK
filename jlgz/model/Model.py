#!/usr/bin/env
# -*-coding:utf8;-*-
#__author__ = 'Mac'

from sqlalchemy import Table, Column, INTEGER, String, Enum, Date, DateTime, VARCHAR, Boolean, TEXT
from sqlalchemy.ext.declarative import declarative_base
from json import dumps
import datetime
from .DBSession import getSession, metadata


class Records(declarative_base()):
    __tablename__ = 'records'

    id = Column(INTEGER(), primary_key=True, autoincrement=True)   #id
    rec_time = Column(DateTime)                              #时间
    content = Column(TEXT)


def add_record(content):
    record = Records()
    if isinstance(content, str):
        record.content = content
    elif isinstance(content, dict):
        record.content = dumps(content, ensure_ascii=False)
    else:
        return -1

    record.rec_time = datetime.datetime.now()

    with getSession() as sess:
        sess.add(record)


def get_record():
    res = []
    with getSession() as sess:
        res = sess.query(Records.content).all()
    return res


records_table = Table('records', metadata,
    Column('id', INTEGER, primary_key=True, autoincrement=True),
    Column('rec_time', DateTime),
    Column('content', TEXT),
)

metadata.create_all()
