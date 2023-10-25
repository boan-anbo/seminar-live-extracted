# Create your views here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView

from djangoProject.host.actions import populate_host_slugname
from djangoProject.host.models import Host
from djangoProject.organization.actions import populate_organization_slugname
from djangoProject.organization.models import Organization
from djangoProject.person.actions import populate_person_slugname
from djangoProject.person.models import Person
from djangoProject.tag.actions import populate_tag_slugname
from djangoProject.tag.filters import TagFilter
from djangoProject.tag.models import Tag
from djangoProject.tag.serializers import TagSerializer


@receiver(post_save, sender=Tag)
def update_tag_slug(sender, instance, **kwargs):
    if kwargs.get('created', False):
        tag = populate_tag_slugname(instance)
        tag.save()
    print("tag slug name updated")


@receiver(post_save, sender=Host)
def update_host_slug(sender, instance, **kwargs):
    if kwargs.get('created', False):
        host = populate_host_slugname(instance)
        host.save()
    print("host slug name updated")

@receiver(post_save, sender=Organization)
def update_organization_slug(sender, instance, **kwargs):
    if kwargs.get('created', False):
        organization = populate_organization_slugname(instance)
        organization.save()
    print("organization slug name updated")

@receiver(post_save, sender=Person)
def update_person_slug(sender, instance, **kwargs):
    if kwargs.get('created', False):
        person = populate_person_slugname(instance)
        person.save()
    print("person slug name updated")

class TagListView(ListAPIView):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class=TagFilter
    pagination_class = None

