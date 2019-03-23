# -*- coding: utf-8 -*-
import csv
import os

from django.core.management.base import BaseCommand

from biocad.models import EquipmentClass, Product, Equipment


class Command(BaseCommand):
    help = 'Import equipment'

    def handle(self, *args, **options):
        data_dir = os.path.join(os.path.dirname(__file__), '../../../data')
        file_path = os.path.join(os.path.normpath(data_dir), 'equipment.tsv')
        with open(file_path) as csvfile:
            rows = csv.reader(csvfile, delimiter='\t')
            next(rows, None)
            for row in rows:
                equipment_id = row[0]
                equipment_class_name = row[1]
                speed_per_hour = row[3]
                equipment_class = EquipmentClass.objects.filter(name=equipment_class_name)
                if not equipment_class:
                    equipment_class = EquipmentClass(name=equipment_class_name)
                    equipment_class.save()
                else:
                    equipment_class = equipment_class[0]
                equipment = Equipment(id=equipment_id,
                                      equipment_class=equipment_class,
                                      speed_per_hour=speed_per_hour)
                equipment.save()
        self.stdout.write('Thats all!')
