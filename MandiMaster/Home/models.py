from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator



# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True,default="avatar.svg")
    is_online = models.BooleanField(default=False)
    phoneNumber = models.CharField(max_length=20)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =  []

class Topic(models.Model):
    name = models.CharField(max_length=122)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=122)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name
    
class Currency(models.Model):
    name = models.CharField(max_length=122)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


class Room(models.Model):    
    host = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)
    Type = models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True)
    Category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
    Image = models.ImageField(null=True)
    Title = models.CharField(max_length=122)
    Price = models.BigIntegerField()
    Currency = models.ForeignKey(Currency, on_delete=models.SET_NULL,null=True)
    Quantity = models.CharField(null=True, max_length=30)
    City = models.CharField(null=True, max_length=30)
    Address = models.CharField(null=True, max_length=128)
    Description = models.TextField(max_length=250,null=True)
    participants = models.ManyToManyField(User, related_name='participants',blank=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created']
    def __str__(self):
        return self.Title

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-updated','-created']
    def __str__(self):
        return self.body[0:50]

