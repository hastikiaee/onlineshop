import json
from django.core.management.base import BaseCommand
from acounts.models import Province, City


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open("iranstates.json", encoding="utf-8") as f:
            data = json.load(f)

            for province,cities in data.items():
                province=Province.objects.create(name=province)
                for city in cities:
                    City.objects.create(name=city,province=province)