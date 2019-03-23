# -*- coding: utf-8 -*-
import csv
import datetime
import os
import sqlite3

from django.core.management.base import BaseCommand

from biocad.models import EquipmentClass, Product, Equipment, Order


class Command(BaseCommand):
    help = 'Import equipment'

    def handle(self, *args, **options):
        data_dir = os.path.join(os.path.dirname(__file__), '../../../')
        file_path = os.path.join(os.path.normpath(data_dir), 'data/order.csv')
        db_path = os.path.join(os.path.normpath(data_dir), 'db.sqlite3')
        Order.objects.all().delete()
        conn = sqlite3.connect(db_path)
        with open(file_path) as csvfile:
            rows = csv.reader(csvfile)
            next(rows, None)
            for row in rows:
                order_id = row[0]
                product_id = row[1]
                amount = row[2]
                deadline = datetime.datetime.strptime(row[3], '%Y-%m-%d')
                conn.execute("""insert into biocad_order(id, product_id, amount, deadline)
                                values ({0}, "{1}", {2}, "{3}")""".format(order_id, product_id, amount, deadline))
                print(order_id, product_id, amount, deadline)
            conn.commit()
        self.stdout.write('Thats all!')