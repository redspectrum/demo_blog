from django.db import models
from django.shortcuts import reverse
from django.core.exceptions import ValidationError
import string
import random
from django.utils.text import slugify
from time import time

def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=150, unique=True)
    body = models.TextField(blank=True, db_index=True)
    date_pub = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    # image = models.ManyToManyField('Image', blank=True, related_name='images')

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']

def generate_filename(instance, filename):
    print(instance)
    print(dir(instance))
    filename = instance.title + '.jpg'
    return "{0}/{1}".format(instance, filename)


class Collection(models.Model):

    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    # image = models.ImageField(blank=True, upload_to='images/main/')
    pictures = models.ManyToManyField('Picture', blank=True, related_name='collection')
    # image = models.ImageField(blank=True, upload_to='images/{}'.format(title))

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('collection_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('collection_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('collection_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']


def minimum_size(width=None, height=None):
    def validator(image):
        if not image.is_image():
            raise ValidationError('File should be image.')

        errors, image_info = [], image.info()['image_info']
        if width is not None and image_info['width'] < width:
            errors.append('Width should be > {} px.'.format(width))
        if height is not None and image_info['height'] < height:
            errors.append('Height should be > {} px.'.format(height))
        raise ValidationError(errors)
    return validator


class Picture(models.Model):

    url = models.ImageField()

    def __str__(self):
        return '{}'.format(self.url)


# class Image(models.Model):
#     slug = models.SlugField(max_length=10, primary_key=True, blank=True)
#     # image = models.ImageField(manual_crop="", validators=[minimum_size(400, 400)])
#     image = models.ImageField(upload_to='media/images/')
#
#     def __repr__(self):
#         return u'<Image slug={0} image={1}>'.format(self.slug, self.image)
#
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = ''.join(random.sample(string.ascii_lowercase, 6))
#         super(Image, self).save(*args, **kwargs)
#
#
#     def get_absolute_url(self):
#         return 'detail', (), {'pk': self.pk}