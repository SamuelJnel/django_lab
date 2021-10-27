from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here
MEALS = (
    ('B', 'Breakfast'),
    ('D', 'Dinner')
)

class Toy(models.Model):
    name = models.CharField(max_length=60)
    color = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'pk': self.id})

class Chinchilla(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    toys = models.ManyToManyField(Toy)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('details', kwargs={'chinchilla_id': self.id})
    
    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)

class Feeding(models.Model):
    date = models.DateField('feeding date')
    meal = models.CharField(
    max_length=1,
    # add the 'choices' field option
    choices=MEALS,
    # set the default value for meal to be 'B'
    default=MEALS[0][0]
  )
    chinchilla = models.ForeignKey(Chinchilla, on_delete=models.CASCADE)

    def __str__(self):
    # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_meal_display()} on {self.date}"
    class Meta:
        ordering = ['-date']



class Photo(models.Model):
    url = models.CharField(max_length=200)
    chinchilla = models.ForeignKey(Chinchilla, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for chinchilla_id: {self.chinchilla_id} @{self.url}"


