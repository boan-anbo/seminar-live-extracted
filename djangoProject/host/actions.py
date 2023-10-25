from uuslug import slugify

from djangoProject.host.models import Host


def populate_host_slugname(host: Host) -> Host:
    slugTitle = slugify(host.name)
    hostWithSameHostName = Host.objects.filter(slugName=slugTitle).exclude(id=host.id)
    if len(hostWithSameHostName) > 0:
        counter = 1
        slugTitle = slugTitle + '_' + str(counter)
        hostWithSameHostName = Host.objects.filter(slugName=slugTitle)
        while len(hostWithSameHostName) > 0:
            counter += 1
            slugTitle = slugTitle + '_' + str(counter)
            hostWithSameHostName = Host.objects.filter(slugName=slugTitle)
    host.slugName = slugTitle
    return host

