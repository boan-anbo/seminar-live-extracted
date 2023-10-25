from django_extensions.management.jobs import BaseJob

from sl2_connect.twitter.test import remove_all_my_tweets


class Job(BaseJob):
    help = 'remove my tweets and twitters records'


    def execute(self):

        remove_all_my_tweets()