# -*- coding: utf-8 -*-

from django.contrib import admin

from biocad.models import EquipmentClass, Product, Equipment, Order


class OrderAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('deadline', )
        return self.readonly_fields


admin.site.register(EquipmentClass)
admin.site.register(Product)
admin.site.register(Equipment)
admin.site.register(Order, OrderAdmin)
