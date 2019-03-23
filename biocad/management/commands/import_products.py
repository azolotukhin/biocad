# -*- coding: utf-8 -*-
import csv
import os

from django.core.management.base import BaseCommand

from biocad.models import EquipmentClass, Product


class Command(BaseCommand):
    help = 'Import products'
    
    def handle(self, *args, **options ):
        data_dir = os.path.join(os.path.dirname(__file__), '../../../data')
        file_path = os.path.join(os.path.normpath(data_dir), 'product.csv')
        with open(file_path) as csvfile:
            rows = csv.reader(csvfile)
            next(rows, None)
            for row in rows:
                product_id = row[0]
                equipment_classes = [v.strip()[1:-1] for v in row[1][1:-1].split(',')]
                product_equipment_classes = []
                for equipment_class_name in equipment_classes:
                    equipment_class = EquipmentClass.objects.filter(name=equipment_class_name)
                    if not equipment_class:
                        equipment_class = EquipmentClass(name=equipment_class_name)
                        equipment_class.save()
                        print(equipment_class_name)
                    else:
                        equipment_class = equipment_class[0]
                    product_equipment_classes.append(equipment_class)
                product = Product(id=product_id)
                product.save()
                product.equipment_classes.add(*product_equipment_classes)

                print(equipment_classes)
        self.stdout.write('Thats all!')