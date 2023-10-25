from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

class CustomAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):
        # fetch custom account confirm url and use it with email confirmation.key = key(0)
        url = settings.CUSTOM_ACCOUNT_CONFIRM_EMAIL_URL.format(emailconfirmation.key)
        # ret = build_absolute_uri(
        #     request,
        #     url)
        ret = settings.MAIN_DOMAIN_NAME + url
        return ret

