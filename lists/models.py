from django.db import models
from django.urls import reverse

class List(models.Model):
    '''Список дел'''

    def get_absolute_url(self):
        '''Получить абсолютный URL'''
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    '''Элемент списка'''
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ['list', 'text']
