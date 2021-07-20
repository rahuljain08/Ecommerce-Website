from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
# Create your models here.

class Company(models.Model):
	name = models.CharField(max_length =  40)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length = 40, unique=True)
	description = models.TextField()
	price = models.IntegerField(validators = [MinValueValidator(0)])
	image = models.ImageField()
	stock = models.IntegerField(validators = [MinValueValidator(0)])
	company = models.ForeignKey('Company', on_delete = models.CASCADE)


	def __str__(self):
		return self.name

class Order(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	product = models.ForeignKey("Product", on_delete = models.CASCADE)
	placed_on = models.DateField(auto_now = True)
	quantity = models.IntegerField(default = 1)
	status = models.CharField(max_length = 20, default = "Processing")
	total_amount = models.IntegerField(validators = [MinValueValidator(0)])

	def __str__(self):
		return self.user.username + " - " + self.product.name

class Cart(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, default = 0)
	product = models.ForeignKey('Product', on_delete = models.CASCADE)
	quantity = models.IntegerField()
	price_per_item = models.IntegerField()
	total = models.IntegerField()

	def __str__(self):
		return self.user.username + " - " + self.product.name

