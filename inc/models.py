import settings
from django.db import models
from datetime import datetime

class BookRaw(models.Model):
    book_raw_id = models.IntegerField(primary_key = True)
    text        = models.TextField()       
    parse_date  = models.DateTimeField(auto_now=True)
    category    = models.CharField(max_length=20)

    class Meta:
        db_table = 'book_raw'

    def getCategoryId(self):
        categories = {'fantasy': 46,
                      'love': 2487,
                      'children': 1415,
                      'poetry': 13,
                      'sf': 36,
                      'detective': 1123,
                      'adventure': 2849,
                      'comedies': 776
                      };
        return categories[self.category]

class Hash(models.Model):
    hash          = models.CharField(max_length=32, primary_key = True)
    experiment_id = models.IntegerField(primary_key = True)
    class_id      = models.IntegerField(primary_key = True)
    count         = models.IntegerField()

    class Meta:
        db_table = 'hash'
