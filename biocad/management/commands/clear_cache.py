# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from biocad.models import cache


class Command(BaseCommand):
    help = 'Import equipment'

    def handle(self, *args, **options):
        cache.delete('schedule_cache')
