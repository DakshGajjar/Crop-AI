from django.db import models

# Create your models here.
class imginput(models.Model):
    img = models.ImageField(upload_to='images/')

class pestimg(models.Model):
    pimg = models.ImageField(upload_to='tempimgs/')