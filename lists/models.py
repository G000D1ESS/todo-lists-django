from django.db import models
from django.urls import reverse
from django.conf import settings


class List(models.Model):
    '''Список дел'''
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        '''Получить абсолютный URL'''
        return reverse('view_list', args=[self.id])

    @property
    def name(self):
        return self.item_set.first().text


class Item(models.Model):
    '''Элемент списка'''
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ['list', 'text']
