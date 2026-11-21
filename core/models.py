
from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):

    ITEM_TYPE = [
        ('Lost', 'Lost'),
        ('Found', 'Found'),
    ]

    ITEM_STATUS = [
        ('Active', 'Active'),
        ('Claimed', 'Claimed'),
        ('Returned', 'Returned'),
    ]

    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Documents', 'Documents'),
        ('Clothing', 'Clothing'),
        ('Bags', 'Bags'),
        ('Accessories', 'Accessories'),
        ('Books', 'Books'),
        ('Other', 'Other'),
    ]

    # Item information
    item_type = models.CharField(
        max_length=10,
        choices=ITEM_TYPE
    )

    item_name = models.CharField(max_length=200)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField()

    location = models.CharField(max_length=200)

    date_lost_found = models.DateField()

    contact_number = models.CharField(max_length=15)

    # Item status
    status = models.CharField(
        max_length=20,
        choices=ITEM_STATUS,
        default='Active'
    )

    # User who reported the item
    reported_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    # Automatically save report date
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name
