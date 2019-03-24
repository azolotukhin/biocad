from django.core.management import BaseCommand

from biocad.models import Equipment, Order, Product
from datetime import datetime as dt
from algo import get_schedule, transform_equipments_sqlite, transform_orders_sqlite, transform_products_sqlite
import numpy as np


class Command(BaseCommand):
    help = 'Import equipment'

    def handle(self, *args, **options):
        print('start')
        equipments = Equipment.objects.all()
        orders = Order.objects.all()
        products = Product.objects.all()

        equipment_dict = transform_equipments_sqlite(equipments)
        products_dict = transform_products_sqlite(products)
        orders_dict = transform_orders_sqlite(orders)

        orders_dict[94237]['execution_restrictions'] = {'start': dt(2019, 3, 20, 15, 40, 0)}
        orders_dict[35233]['execution_restrictions'] = {'equipment': '3d793be1-90fa-11e1-818a-b614f2bbba79'}
        orders_dict[75612]['execution_restrictions'] = {'start': dt(2019, 3, 27, 10, 0, 15),
                                                        'equipment': '42b5beb2-2550-11e1-9589-b614f2bbba79'}
        print("start calculating schedule..")
        schedule = get_schedule(equipment_dict, orders_dict, products_dict)
        print(schedule["orders_stat"][94237])
        print(schedule["orders_stat"][35233])
        print(schedule["orders_stat"][75612])
        print("end calculating schedule")
        n_successes = np.sum([order['is_placed']
                              for order in schedule['orders_stat'].values()])
        # print(max_order_price, n_successes)
        print(n_successes)
