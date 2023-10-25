from django_filters import rest_framework as filters

from djangoProject.person.models import Person


class PersonFilter(filters.FilterSet):
    # tagType = ChoiceFilter(choices=TagType)

    class Meta:
        model = Person
        fields = ['firstName', 'lastName']