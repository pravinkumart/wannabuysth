# -*- coding: UTF-8 -*-
import sys
import os

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

sys.path.insert(0, '../')
sys.path.insert(0, '../../')

from models import Catalog
from models import SubCataog

from models import Merchant
from models import Product

catalog_list = []
catalog_list.append(['index_1.png', '保健', ['女性保健', '男性保健', '四季保健', '饮食保健']])
catalog_list.append(['index_2.png', '家政', ['小时工', '钟点工', '保洁', '护工']])
catalog_list.append(['index_3.png', '旅游', ['九寨沟', '海螺沟', '峨眉']])
catalog_list.append(['index_4.png', '母婴', ['保姆', '月嫂', '育婴']])
catalog_list.append(['index_5.png', '汽车', []])
catalog_list.append(['index_6.png', '租房', ['经济适用房', '两限两竞房', '保障性住房', '合租房']])
catalog_list.append(['index_7.png', '金融', ['证券', '基金', '保险', '信托']])


def init_data():
    from wannabuysth import Session
    session = Session()
    for catalog in catalog_list:
        c = Catalog(name=catalog[1], descp='', icon_smaill='../static/data/' + catalog[0], icon_large='../static/data/' + catalog[0], idx=0)
        catalog_id = c.id
        session.add(c)
        for rec in catalog[2]:
            s = SubCataog(catalog_id=catalog_id, catalog=c, name=rec, descp='', icon_smaill='', icon_large='', idx=0)
            session.add(s)
        session.commit()
    session.close()



if __name__ == '__main__':
    init_data()
