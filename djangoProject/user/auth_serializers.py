from dj_rest_auth.serializers import PasswordResetSerializer
from rest_framework.request import Request


class MyPasswordResetSerializer(PasswordResetSerializer):

    def get_email_options(self):
        request: Request = self.context.get('request')
        print(request)
        domain = request.get_host()
        print(domain)
        super().get_email_options()
        return {

            'subject_template_name': 'email/password_reset_key_subject.txt',
            'email_template_name': 'email/password_reset_key_message.txt',
        }