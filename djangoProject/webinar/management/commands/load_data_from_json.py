from django.core.management import BaseCommand

from djangoProject.organization.models import Organization


class Command(BaseCommand):
    help = 'load_data_from_json'

    def handle(self, *args, **options):
        for x in range(0, 50):
            org = Organization()
            org.name = 'test'
            org.save()
