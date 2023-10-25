from django.contrib import admin
# Register your models here.
# Register your models here.
from django.contrib.admin import TabularInline

# admin.site.register(Tag)
from djangoProject.profilefilter.models import ProfileFilter
from djangoProject.submission.models import Submission
from djangoProject.userprofile.models import UserProfile


class ProfileFilterInline(TabularInline):
    model = ProfileFilter

class SubmissionInline(TabularInline):
    model = Submission

    show_change_link = True

class UserProfileAdmin(admin.ModelAdmin):

    list_per_page = 25

    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    list_editable = ['isTagger', 'isRecommender', 'isDirectPoster', 'isLeadCollector']
    filter_horizontal = ['savedWebinars' ]
    list_filter = ['isTagger', 'isRecommender', 'isDirectPoster', 'isLeadCollector']

    list_display = ['id', 'user', 'isTagger', 'isRecommender','isDirectPoster', 'isLeadCollector','currentView', 'timezone', 'language', 'karma' ]
    fields = ['user', 'isTagger', 'isRecommender', 'isDirectPoster', 'currentView', 'timezone', 'language', 'karma']
    change_links = ['user']
    changelist_links = ['user']
    inlines = [ProfileFilterInline, SubmissionInline]




admin.site.register(UserProfile, UserProfileAdmin)
