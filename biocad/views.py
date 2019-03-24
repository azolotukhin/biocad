# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render

from algo import get_schedule, transform_equipments_sqlite, transform_products_sqlite, transform_orders_sqlite
from biocad.models import Equipment, Order, Product


def index(request):
    equipments = Equipment.objects.all()
    orders = Order.objects.all()
    products = Product.objects.all()

    equipment_dict = transform_equipments_sqlite(equipments)
    products_dict = transform_products_sqlite(products)
    orders_dict = transform_orders_sqlite(orders)

    schedule = get_schedule(equipment_dict, orders_dict, products_dict)
    shedule_for_date = {}
    filter_date = datetime.datetime(2019, 4, 19).date()
    for equipment_id, data in schedule['equipment_schedule'].items():
        shedule_for_date[equipment_id] = []
        for d in data:
            if d['start'].date() == filter_date:
                if d['end'].date() > filter_date:
                    d['end'] = datetime.datetime.combine(filter_date, datetime.datetime.max.time())
                shedule_for_date[equipment_id].append(d)
            elif d['end'].date() == filter_date:
                d['start'] = datetime.datetime.combine(filter_date, datetime.datetime.min.time())
                shedule_for_date[equipment_id].append(d)
        # shedule_for_date[equipment_id] = [d for d in data if d['start'].date() == datetime.datetime.utcnow().date()]
    return render(request, 'index.html', {'schedule': shedule_for_date})
