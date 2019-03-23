# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render

from algo import get_schedule
from biocad.models import Equipment, Order, Product


def index(request):
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
        shedule_for_date[equipment_id] = [d for d in data if d['start'].date() == datetime.datetime.utcnow().date()]
    return render(request, 'index.html', {'schedule': shedule_for_date})