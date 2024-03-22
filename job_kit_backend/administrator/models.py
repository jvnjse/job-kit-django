from django.db import models

# Create your models here.
class JobCategory(models.Model):
    category_name = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name