from django.core.management import BaseCommand

from djangoProject.host.actions import populate_host_slugname
from djangoProject.host.models import Host
from djangoProject.organization.actions import populate_organization_slugname
from djangoProject.organization.models import Organization
from djangoProject.person.actions import populate_person_slugname
from djangoProject.person.models import Person
from djangoProject.tag.actions import populate_tag_slugname
from djangoProject.tag.models import Tag


class Command(BaseCommand):
    help = 'populate filter slugnames'

    def handle(self, *args, **options):
        tags = Tag.objects.all()

        for tag in tags:
            if tag.slugName is None:
                tagWithSlugName = populate_tag_slugname(tag)
                tagWithSlugName.save()
                print(tag.slugName)
                print(tagWithSlugName.slugName)
        persons = Person.objects.all()
        for person in persons:
            if person.slugName is None or len(person.slugName) == 0:
                personWithSlugName = populate_person_slugname(person)
                personWithSlugName.save()
                print(personWithSlugName.slugName)

        hosts = Host.objects.all()
        for host in hosts:
            if host.slugName is None or len(host.slugName) == 0:
                hostWithSlugName = populate_host_slugname(host)
                hostWithSlugName.save()
                print(hostWithSlugName.slugName)

        orgs = Organization.objects.all()
        for org in orgs:
            # if org.slugName is None or len(org.slugName) == 0:
            orgWithSlugName = populate_organization_slugname(org)
            orgWithSlugName.save()
            print(orgWithSlugName.slugName)
