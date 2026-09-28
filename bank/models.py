from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=50,unique=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    passport_id = models.CharField(max_length=50,unique=True)
    balance = models.IntegerField(default=1000)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16,unique=True)
    cvv = models.CharField(max_length=3)
    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=50)
    pin = models.CharField(max_length=4)
    balance = models.IntegerField(default=500)
    def __str__(self):
        return self.card_number

class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sent_transactions')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name='received_transactions')
    source = models.CharField(max_length=20)
    source_card = models.ForeignKey(Card, on_delete=models.CASCADE,null=True, blank=True,related_name='source_transactions')
    destination = models.CharField(max_length=20)
    destination_card = models.ForeignKey(Card, on_delete=models.CASCADE,null=True, blank=True,related_name='destination_transactions')
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return str(self.amount)