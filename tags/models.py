from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label

class TaggedItem(models.Model):
    # what tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    '''
    we don't want to make this model dependent upon shop.product
    So we use generic objects and relation ship from django.contrib.contenttypes.models
    We need two info to determine the object we want to tag it
    1. Type (product, articles, blog, news, videos, etc) ---> content_type 
    2. ID ---> object id
    3. generic foreigh relation --> content_object
    Its limitation is it works only if the id is the integer
    '''
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)#type of object
    object_id = models.PositiveIntegerField()# id of the object
    content_object = GenericForeignKey()
