from uuslug import slugify

from djangoProject.organization.models import Organization


def populate_organization_slugname(organization: Organization) -> Organization:
    currentName = ''
    if organization.name and len(organization.name) > 0:
        currentName = organization.name
    if len(currentName) == 0:
        if organization.nameCn and len(organization.nameCn) > 0:
            currentName = organization.nameCn
        else:
            raise Exception('No propern ame')
    slugName = slugify(currentName)
    organizationWithSameHostName = Organization.objects.filter(slugName=slugName).exclude(id=organization.id)
    if len(organizationWithSameHostName) > 0:
        counter = 1
        slugName = slugName + '_' + str(counter)
        organizationWithSameHostName = Organization.objects.filter(slugName=slugName)
        while len(organizationWithSameHostName) > 0:
            counter += 1
            slugName = slugName + '_' + str(counter)
            organizationWithSameHostName = Organization.objects.filter(slugName=slugName)
    organization.slugName = slugName
    return organization