from django.db import models
from django.db.models import CASCADE
from datetime import date 

# Create your models here.
class company(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    about = models.TextField()
    type = models.CharField(max_length=50,choices=(('IT','IT'),('NON IT','NON IT'),('PHONE NO','PHONE NO')))
    added_Date= models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name + "-" + self.location 

class employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=150)
    phone_no = models.CharField(max_length=10)
    position = models.CharField(max_length=50,choices=(('Manager','Manager'),('Software Developer','Software Developer'),('Project Leader','Project Leader')))
    salary = models.DecimalField(max_digits=9,decimal_places=2)
    join_date = models.DateField()
    company = models.ForeignKey(company,on_delete=CASCADE)

    def __str__(self):
        return self.name + "-" + self.position