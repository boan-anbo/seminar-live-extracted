from django.core.management import BaseCommand
from pypinyin.core import lazy_pinyin

from djangoProject.host.actions import populate_host_slugname
from djangoProject.host.models import Host
from djangoProject.organization.actions import populate_organization_slugname
from djangoProject.organization.models import Organization
from djangoProject.person.actions import populate_person_slugname
from djangoProject.person.models import Person
from djangoProject.tag.actions import populate_tag_slugname
from djangoProject.tag.models import Tag


class Command(BaseCommand):
    help = 'populate tag name pinyin'

    def handle(self, *args, **options):
        tags = Tag.objects.all()

        for tag in tags:
            pinyin = ' '.join(lazy_pinyin(tag.nameCn))
            tag.namePinyin = pinyin
            tag.save()
