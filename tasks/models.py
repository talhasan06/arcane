from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
import pytz
# Create your models here.

class Category(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100,unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate slug if it is not provided
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Task(models.Model):
    PRIORITY_CHOICES =[
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True,blank=True)
    due_time = models.TimeField(null=True,blank=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    completed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Set created_date to Dhaka local time when the object is saved
        dhaka_tz = pytz.timezone('Asia/Dhaka')
        self.created_date = timezone.datetime.now(dhaka_tz)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title