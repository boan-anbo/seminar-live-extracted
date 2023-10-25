from rest_framework import serializers

from djangoProject.person.models import Person


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    # organizer_webinars = WebinarSerializer(many=True, required=False)

    class Meta:
        model = Person
        fields = ['id', 'firstName', 'firstNameCn', 'lastName', 'lastNameCn', 'slugName']

# class PersonSerializerWithOrganizerWebinars(serializers.HyperlinkedModelSerializer):
#     # organizer_webinars = WebinarSerializer(many=True, required=False)
#
#     class Meta:
#         model = Person
#     fields = ['id', 'firstName', 'lastName', 'organizers']
#
# class PersonSerializerWithParticipantWebinars(serializers.HyperlinkedModelSerializer):
#     # organizer_webinars = WebinarSerializer(many=True, required=False)
#
#     class Meta:
#         model = Person
#     fields = ['id', 'firstName', 'lastName', 'participants']