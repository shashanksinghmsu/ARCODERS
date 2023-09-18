def create_slug(instance, new_slug=None):
    temp = instance.title

    slug_list = temp.split(" ")
    separator = "-"
    temp_slug = separator.join(slug_list)
    slug_list = temp_slug.split('/')
    temp = '_'.join(slug_list)

    slug = slugify(temp)
    if new_slug is not None:
        slug = new_slug
    qs = programTitle.objects.filter(slug=slug).order_by("-titleId")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().titleId)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_program(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_program, sender=programTitle)
