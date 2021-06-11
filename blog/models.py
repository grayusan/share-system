from users.models import CustomUser
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from typing import Iterable

# Create your models here.

class ListField(models.TextField):
    """
    A custom Django field to represent lists as comma separated strings
    """

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['token'] = self.token
        return name, path, args, kwargs

    def to_python(self, value):

        class SubList(list):
            def __init__(self, token, *args):
                self.token = token
                super().__init__(*args)

            def __str__(self):
                return self.token.join(self)

        if isinstance(value, list):
            return value
        if value is None:
            return SubList(self.token)
        return SubList(self.token, value.split(self.token))

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        if not value:
            return
        assert(isinstance(value, Iterable))
        return self.token.join(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

class Post(models.Model):
    title = models.CharField(max_length=70)
    text = models.TextField('text')
    # author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField('Created date', default=timezone.now)  
    published_date = models.DateTimeField(blank=True, null=True)
    allowed_list = ListField()

    def get_absolute_url(self):
        return reverse('blog:blog-home')

    def __str__(self):
        return self.title

class Document(models.Model):
    id = models.BigAutoField(primary_key=True,unique=True)
    name = models.CharField(max_length=255, blank=False)
    document = models.FileField(upload_to='documents/')
    target = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='taget-post')
    created_at = models.DateTimeField('created_date', default=timezone.now)

    def __str__(self):
        return self.name