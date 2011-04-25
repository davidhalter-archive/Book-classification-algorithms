import settings
from django.db import models
from datetime import datetime
import category

class BookRaw(models.Model):
    book_raw_id = models.IntegerField(primary_key = True)
    text        = models.TextField()       
    parse_date  = models.DateTimeField(auto_now=True)
    category    = models.CharField(max_length=20)

    class Meta:
        db_table = 'book_raw'

    def getCategoryId(self):
        return category.get_category_id(self.category)


class Hash(models.Model):
    hash_id       = models.AutoField(primary_key = True)
    hash          = models.CharField(max_length=32)
    experiment_id = models.IntegerField()
    class_id      = models.IntegerField()
    count         = models.IntegerField()
    text          = models.TextField(null = True)

    class Meta:
        db_table = 'hash'
