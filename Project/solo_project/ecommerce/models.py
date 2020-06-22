from django.db import models
import re

class Manager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name_len'] = "First name should be at least 2 characters."
        if not postData['first_name'].isalpha():
            errors['first_name_alpha'] = "First Name cannot contain numbers or special characters."
        if len(postData['last_name']) < 2:
            errors['last_name_len'] = "Last name should be at least 2 characters."
        if not postData['last_name'].isalpha():
            errors['last_name_alpha'] = "Last Name cannot contain numbers or special characters."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = ("Invalid email address!")
        if User.objects.filter(email=postData['email']).exists():
            errors['emailunique'] = "Email already registered, please login."
        if postData['password'] != postData['confirmpw']:
            errors['pwmatch'] = "Passwords must match."
        if len(postData['password']) < 10:
            errors['pwlen'] = "Password should be at least 10 characters."
        if postData['password'].isalpha():
            errors['pwtest'] = "Password must contain numbers and/or special characters."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=70)
    password = models.TextField()
    objects = Manager()

class Order(models.Model):
    color = models.CharField(max_length=6)
    shipname = models.CharField(max_length=150)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    quantity = models.IntegerField()
    price = models.FloatField()
    ordered_by = models.ForeignKey(User, related_name="orders", on_delete = models.CASCADE)
