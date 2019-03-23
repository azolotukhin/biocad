# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render

from algo import get_schedule
from biocad.models import Equipment, Order, Product


def index(request):
    filter_date = datetime.datetime.today().date()
    filter_date_str = request.GET.get('date', '')
    if filter_date_str:
        try:
            filter_date = datetime.datetime.strptime(filter_date_str, '%d.%m.%Y').date()
        except:
            pass
    equipments = Equipment.objects.all()
    orders = Order.objects.all()
    products = Product.objects.all()

    equipment_dict = {eq.id: {'class': eq.equipment_class.name, 'speed': eq.speed_per_hour}
                      for eq in equipments}

    products_dict = {pr.id: [cl.name for cl in pr.equipment_classes.all()]
                     for pr in products}
    orders_dict = {order.id: {'product_id': order.product_id,
                              'amount': order.amount,
                              'deadline': order.deadline
                              }
                   for order in orders}
    schedule = get_schedule(equipment_dict, orders_dict, products_dict)
    shedule_for_date = {}
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
    return render(request, 'index.html', {'schedule': shedule_for_date,
                                          'filter_date': filter_date})