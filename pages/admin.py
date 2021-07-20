from django.contrib import admin
from pages import models
# Register your models here.
admin.site.register([
	models.Company,
	models.Product,
	models.Order,
	models.Cart
])