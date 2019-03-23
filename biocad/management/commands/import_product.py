# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Import products'
    
    def handle(self, *args, **options ):
        orders = Order.objects.filter(comment__isnull=False)
        for order in orders:
            if order.comment:
                site_id = settings.SITE_ID
                content_type = ContentType.objects.get_for_model(Order)
                comment = Comment.objects.create(object_pk=order.id,
                                                  content_type=content_type,
                                                  comment=order.comment,
                                                  site_id=site_id)
        self.stdout.write('Thats all!')