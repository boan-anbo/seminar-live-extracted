from djangoProject.person.models import Person
from uuslug import slugify

def populate_person_slugname(person: Person) -> Person:
    slugName = slugify(person.firstName + ' ' + person.lastName)
    personWithSameHostName = Person.objects.filter(slugName=slugName).exclude(id=person.id)
    if len(personWithSameHostName) > 0:
        counter = 1
        slugName = slugName + '_' + str(counter)
        personWithSameHostName = Person.objects.filter(slugName=slugName)
        while len(personWithSameHostName) > 0:
            counter += 1
            slugName = slugName + '_' + str(counter)
            personWithSameHostName = Person.objects.filter(slugName=slugName)
    person.slugName = slugName
    return person