from django.db import models


class Item(models.Model):
    id = models.BigAutoField(primary_key=True)
    item_name = models.CharField(max_length=100)
    item_price = models.IntegerField()
    item_image_url = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100, default='')
    option_name = models.CharField(max_length=100, default='')

    class Meta:
        db_table = 'item'