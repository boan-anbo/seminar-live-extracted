from django.contrib.auth.models import User

from djangoProject.userprofile.models import UserProfile


def get_profile_by_user(user: User) -> UserProfile:
    return UserProfile.objects.get(user=user)