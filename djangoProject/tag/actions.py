from uuslug import slugify

from djangoProject.tag.models import Tag


def populate_tag_slugname(tag: Tag) -> Tag:
    slugTitle = slugify(tag.name)
    tagWithSameTagName = Tag.objects.filter(slugName=slugTitle).exclude(id=tag.id)
    if len(tagWithSameTagName) > 0:
        counter = 1
        slugTitle = slugTitle + '_' + str(counter)
        tagWithSameTagName = Tag.objects.filter(slugName=slugTitle)
        while len(tagWithSameTagName) > 0:
            counter += 1
            slugTitle = slugTitle + '_' + str(counter)
            tagWithSameTagName = Tag.objects.filter(slugName=slugTitle)
    tag.slugName = slugTitle
    return tag