from django.core.management import BaseCommand

from biocad.models import Equipment, Order, Product
from algo import get_schedule


class Command(BaseCommand):
    help = 'Import equipment'

    def handle(self, *args, **options):
        print('start')
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

        print("start calculating schedule..")
        schedule = get_schedule(equipment_dict, orders_dict, products_dict)
        print("end calculating schedule")
