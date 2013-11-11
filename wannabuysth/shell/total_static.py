# -*- coding: UTF-8 -*-

from models import Statistics
from models import Merchant
from models import Customer
from models import SuccessRequirment
from wannabuysth import Session

import datetime


def mc_statistics():
    '''
    @note: 商家数量统计
    '''
    now = datetime.datetime.now()
    to_day = now.date()
    start_day = to_day.replace(day=1)
    db = Session()
    count = db.query(Merchant).count()
    rec = db.query(Statistics).filter(Statistics.type == 0, Statistics.cur_day == start_day).first()
    if rec:
        rec.value = count
        db.add(rec)
        db.commit()
    else:
        rec = Statistics(type=0, cur_day=start_day, value=count)
        db.add(rec)
        db.commit()

def cu_statistics():
    '''
    @note: 用户数量统计
    '''
    now = datetime.datetime.now()
    to_day = now.date()
    start_day = to_day.replace(day=1)
    db = Session()
    count = db.query(Customer).count()
    rec = db.query(Statistics).filter(Statistics.type == 1, Statistics.cur_day == start_day).first()
    if rec:
        rec.value = count
        db.add(rec)
        db.commit()
    else:
        rec = Statistics(type=1, cur_day=start_day, value=count)
        db.add(rec)
        db.commit()

def su_statistics():
    '''
    @note: 成交金额
    '''
    now = datetime.datetime.now()
    to_day = now.date()
    start_day = to_day.replace(day=1)
    db = Session()
    datas = db.query(SuccessRequirment).all()
    count = 0
    for data in datas:
        count += data.succes_fee
    rec = db.query(Statistics).filter(Statistics.type == 2, Statistics.cur_day == start_day).first()
    if rec:
        rec.value = count
        db.add(rec)
        db.commit()
    else:
        rec = Statistics(type=2, cur_day=start_day, value=count)
        db.add(rec)
        db.commit()

if __name__ == '__main__':
    mc_statistics()
    cu_statistics()
    su_statistics()
    print '--over---'
