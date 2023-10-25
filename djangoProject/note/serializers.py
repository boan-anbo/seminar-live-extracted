from rest_framework import serializers

# Register your models here.
from djangoProject.note.models import Note


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    authorName = serializers.SerializerMethodField()
    authorId = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Note
        fields = ['id', 'content', 'created', 'modified', 'authorName', 'authorId',  'isAnonymous', 'helpfulness']

    # order of display names:
    # 1. Anonymous if isAnonymous
    # 2. display_name is it is set
    # 3. author's user's username if set
    # 4. author's user's email.
    def get_authorName(self, obj: Note):
        if obj.isAnonymous:
            return 'Anonymous'
        name = obj.author.displayName
        if len(name) == 0:
            name = obj.author.user.__str__()
            if name is None:
                name = obj.author.user.email
        return name

    # class UserSerializer(serializers.ModelSerializer):
    #
    #     class Meta:
    #         model = User
    #
    #     def get_days_since_joined(self, obj):
    #         return (now() - obj.date_joined).days