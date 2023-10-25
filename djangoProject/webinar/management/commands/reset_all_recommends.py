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
from djangoProject.webinar.const import RECOMMEND_LEVEL
from djangoProject.webinar.models import Webinar


class Command(BaseCommand):
    help = 'reset all recommendations'

    def handle(self, *args, **options):
        webinars = Webinar.objects.all()

        for webinar in webinars:
            webinar.recommend = RECOMMEND_LEVEL.NORMAL
            webinar.save()