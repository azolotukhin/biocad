# -*- coding: utf-8 -*-
import datetime
import pickle

from django.shortcuts import render, get_object_or_404

from algo import get_schedule, transform_equipments_sqlite, transform_products_sqlite, transform_orders_sqlite
from biocad.models import Equipment, Order, Product

from biocad.models import Equipment, Order, Product, EquipmentClass, cache


def _get_data_to_cache():
    try:
        data = cache.get('schedule_cache', )
        if data:
            data = pickle.loads(data)
        return data
    except Exception as e:
        return None


def _set_data_to_cache(data):
    try:
        cache.set('schedule_cache', pickle.dumps(data), ex=60)
    except:
        pass


def index(request):
    filter_date = datetime.datetime.today().date()
    filter_date_str = request.GET.get('date', '')
    if filter_date_str:
        try:
            filter_date = datetime.datetime.strptime(filter_date_str, '%d.%m.%Y').date()
        except:
            pass

    equipment_class_id = request.GET.get('equipment_class', '')
    current_equipments_ids = []
    if equipment_class_id:
        try:
            equipment_class = EquipmentClass.objects.get(pk=int(equipment_class_id))
        except:
            equipment_class_id = ''
        else:
            current_equipments = Equipment.objects.filter(equipment_class=equipment_class)
            current_equipments_ids = [e.id for e in current_equipments]

    equipment_classes = EquipmentClass.objects.all()
    schedule = _get_data_to_cache()
    if not schedule:
        equipments = Equipment.objects.all()
        orders = Order.objects.all()
        products = Product.objects.all()

        equipment_dict = transform_equipments_sqlite(equipments)
        products_dict = transform_products_sqlite(products)
        orders_dict = transform_orders_sqlite(orders)

        schedule = get_schedule(equipment_dict, orders_dict, products_dict)
        _set_data_to_cache(schedule)

    shedule_for_date = {}
    for equipment_id, data in schedule['equipment_schedule'].items():
        if current_equipments_ids and equipment_id not in current_equipments_ids:
            continue

        shedule_for_date[equipment_id] = []
        for d in data:
            if d['start'].date() == filter_date:
                d['real_start'] = d['start']
                d['real_end'] = d['end']
                if d['end'].date() > filter_date:
                    d['end'] = datetime.datetime.combine(filter_date, datetime.datetime.max.time())
                shedule_for_date[equipment_id].append(d)
            elif d['end'].date() == filter_date:
                d['real_start'] = d['start']
                d['real_end'] = d['end']
                d['start'] = datetime.datetime.combine(filter_date, datetime.datetime.min.time())
                shedule_for_date[equipment_id].append(d)
        # shedule_for_date[equipment_id] = [d for d in data if d['start'].date() == datetime.datetime.utcnow().date()]

    return render(request, 'index.html', {'schedule': shedule_for_date,
                                          'filter_date': filter_date,
                                          'size': max(200, len(shedule_for_date) * 20),
                                          'equipment_class_id': equipment_class_id,
                                          'equipment_classes': equipment_classes})


def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    schedule = _get_data_to_cache()
    if not schedule:
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
        _set_data_to_cache(schedule)

    order_stat = schedule['orders_stat'][order_id]
    return render(request, 'order.html', {'order': order,
                                          'order_stat': order_stat})
