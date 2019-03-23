# -*- coding: utf-8 -*-
import uuid

from django.db import models


class EquipmentClass(models.Model):
    name = models.CharField(verbose_name='Класс оборудования', max_length=256)

    class Meta:
        verbose_name = 'Класс оборуования'
        verbose_name_plural = 'Классы оборудования'
        ordering = ('name', )

    def __str__(self):
        return self.name


class Equipment(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=256)
    equipment_class = models.ForeignKey(EquipmentClass, on_delete=models.CASCADE, verbose_name='Класс оборудования')
    speed_per_hour = models.IntegerField(default=0, verbose_name='Скорость')
    start_maintenance = models.DateTimeField(verbose_name='Начало тех. работ', blank=True, null=True)
    end_maintenance = models.DateTimeField(verbose_name='Конец тех. работ', blank=True, null=True)

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'
        ordering = ('equipment_class', )

    def __str__(self):
        return self.id


class Product(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=256, editable=False)
    equipment_classes = models.ManyToManyField(EquipmentClass)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.id


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    amount = models.IntegerField(default=0, verbose_name='Количество')
    deadline = models.DateTimeField(verbose_name='Дедлайн')
    start_work_datetime = models.DateTimeField(verbose_name='Начало работы', blank=True, null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='Оборудование', blank=True, null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('deadline',)

    def __str__(self):
        return '%s (%s)' % (self.id, self.deadline.strftime('%Y-%m-%d'))
