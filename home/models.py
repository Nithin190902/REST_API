from django.db import models

#Create your models here.
class Color(models.Model):
    color_name =models.CharField(max_length=50)

    def __str__(self):
        return self.color_name

class PersonModel(models.Model):
    color = models.ForeignKey(Color, null=True, blank=True, on_delete=models.CASCADE, related_name='color')
    name = models.CharField(max_length=50)
    age = models.IntegerField()

    def __str__(self):
        return self.name
    

