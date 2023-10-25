# admin.site.register(Tag)
from django.contrib import admin

from djangoProject.person.models import Person


class PersonAdmin(admin.ModelAdmin):
    filter_horizonal = ['speakers']
    # autocomplete_fields = ['speakers']
    search_fields = ['firstName', 'lastName', 'firstNameCn', 'lastNameCn']
    list_display = ['id','firstName', 'lastName']
    list_display_links = ['id']
    fields = ['id','firstName', 'lastName', 'firstNameCn','lastNameCn', 'slugName']
    readonly_fields = ['id']


# class WebinarAdminForm(forms.ModelForm):
#
#     Organizers = forms.ModelMultipleChoiceField(
#         queryset=Person.objects.all(),
#         required=False,
#         widget=FilteredSelectMultiple(
#             verbose_name=ugettext_lazy('Organizers'),
#             is_stacked=False
#         )
#     )
#
#     class Meta:
#         model = Webinar
#         exclude = []
#
#     def __init__(self, *args, **kwargs):
#         super(WebinarAdminForm, self).__init__(*args, **kwargs)
#
#         if self.instance and self.instance.pk:
#             self.fields['organizers'].initial = self.instance.organizers.all()
#
#     def save(self, commit=True):
#         Webinar = super(WebinarAdminForm, self).save(commit=False)
#
#         if commit:
#             Webinar.save()
#
#         if Webinar.pk:
#             # Webinar.tags = self.cleaned_data['tags']
#             Webinar.tags.set(self.cleaned_data['organizers'])
#             self.save_m2m()
#
#         return Webinar
#
#
# class WebinarAdmin(admin.ModelAdmin):
#     form = WebinarAdminForm


# admin.site.register(Webinar, WebinarAdmin)

admin.site.register(Person, PersonAdmin)
