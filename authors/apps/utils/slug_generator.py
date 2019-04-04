from django.utils.text import slugify


class Slug():
    def generate_unique_slug(self, klass, field):
        """
        method generates a new unigue slug
        """
        origin_slug = slugify(field)
        unique_slug = origin_slug
        numb = 1
        while klass.objects.filter(slug=unique_slug).exists():
            unique_slug = '%s-%d' % (origin_slug, numb)
            numb += 1
        return unique_slug
