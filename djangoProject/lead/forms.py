from admin_object_actions.forms import AdminObjectActionForm
from django import forms

from djangoProject.lead.models import Lead


class LeadObjectActionForm(AdminObjectActionForm):

    confirm = forms.BooleanField()

    class Meta:
        model = Lead
        fields = ()

    def do_object_action(self):
        self.instance.action()

