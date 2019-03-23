# -*- coding: utf-8 -*-
import uuid

from django.db import models


class EquipmentClass(models.Model):
    name = models.CharField(verbose_name='Класс оборудования')


class Equipment(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4)
    class_name = models.CharField(verbose_name='Класс оборудования')
    speed_per_hour = models.IntegerField(default=0, verbose_name='Скорость')


class Product(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4)


class Order(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    amount = models.IntegerField(default=0, verbose_name='Количество')
    deadline = models.DateTimeField(auto_now_add=True, verbose_name='Дедлайн')
