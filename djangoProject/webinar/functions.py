import datetime
from random import randrange

from djangoProject.host.models import Host
from djangoProject.organization.models import Organization
from djangoProject.person.models import Person
from djangoProject.speaker.models import Speaker
from djangoProject.tag.models import Tag
from djangoProject.talk.models import Talk
from djangoProject.webinar.models import Webinar


# get random webinar
def generate_webinar(index: int) -> Webinar:
    random_webinar = Webinar()
    random_webinar.title = "sample webiar " + str(index)
    random_webinar.startDateTimeUTC = datetime.datetime.now() + datetime.timedelta(days=randrange(50))
    random_webinar.startDateTimeUTC = random_webinar.startDateTimeUTC + datetime.timedelta(hours=randrange(24))
    random_webinar.startDateTimeUTC = random_webinar.startDateTimeUTC + datetime.timedelta(minutes=randrange(0, 60, 30))

    random_webinar.description = "This is a description for webinar No." + str(index)

    random_webinar.save()

    # tag = Tag()
    #
    # tag.name = 'Test'
    #
    # tag.save()
    #
    # talk = Talk()
    #
    # talk.title = "First talk"
    #
    # talk.save()
    #
    # person = Person()
    #
    # person.firstName = "First Name"
    #
    # person.lastName = "Last Name"
    #
    # person.save()
    #
    #
    # speaker = Speaker()
    #
    # speaker.person = person
    #
    # speaker.save()
    #
    # talk.speakers.add(speaker)
    #
    # talk.webinar = random_webinar
    #
    # talk.save()
    #
    # # random_webinar.talks.add(talk)
    #
    # # random_webinar.save()
    #
    # organization = Organization()
    #
    # organization.name = 'Yale University'
    #
    # organization.save()
    #
    # host = Host()
    # host.name = "East Asian Languages and Literatures"
    # host.save()
    #
    # host.organizations.add(organization)
    #
    # host.save()

    # random_webinar.hosts.add(host)

    return random_webinar