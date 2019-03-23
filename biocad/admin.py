# -*- coding: utf-8 -*-

from django.contrib import admin

from biocad.models import EquipmentClass, Product, Equipment, Order

admin.site.register(EquipmentClass)
admin.site.register(Product)
admin.site.register(Equipment)
admin.site.register(Order)
