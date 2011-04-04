import settings
from django.db import models
from datetime import datetime

class BookRaw(models.Model):
    book_raw_id = models.IntegerField(primary_key = True)
    text_raw    = models.TextField()       
    text        = models.TextField(null=True) 
    parse_date  = models.DateTimeField(auto_now=True)
    category    = models.CharField(max_length=20)

    class Meta:
        db_table = 'book_raw'
