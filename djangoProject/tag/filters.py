from django_filters import rest_framework as filters

from djangoProject.tag.models import Tag


class TagFilter(filters.FilterSet):
    # tagType = ChoiceFilter(choices=TagType)

    class Meta:
        model = Tag
        fields = ['name', 'tagType']