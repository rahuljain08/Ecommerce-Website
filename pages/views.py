from django.shortcuts import render
from pages import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView
from django.http import HttpResponseBadRequest, HttpResponseServerError, HttpResponse
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
import json
# Create your views here.
def index(request):

	context = {
		"companies": models.Company.objects.all()
	}

	return render(request, "pages/index.html", context)

def about(request):
	context = {
		"page": "About Us"
	}
	return render(request, "pages/about.html", context)

class All_Products(ListView):
	model = models.Product
	def get_context_data(self):
		context = super().get_context_data()
		context["page"] = "All Products"
		return context
	context_object_name = "products"
	template_name = "pages/show_products.html"


class Specific_Product(LoginRequiredMixin, View):

	def get_login_url(self):
		return "/auth/login"

	def get(self, request, pk):
		try:
			products = models.Product.objects.filter(company = pk)
			
			context = {
				"products": products,
				"page": models.Company.objects.get(id = pk)
			}

			return render(request, "pages/show_products.html", context)

		except:
			return HttpResponseBadRequest("Company does not exist!")


class Buy_Product(LoginRequiredMixin, View):

	def get_login_url(self):
		return "/auth/login"

	def get(self, request, pk):
		try:
			product = models.Product.objects.get(id = pk)
			context = {"product": product}
			return render(request, "pages/buy_product.html", context)

		except Exception as e:
			print(e)
			return HttpResponseBadRequest("Product does not exist!")

	def post(self, request, pk):
		try:
			p = models.Product.objects.get(id = pk)
			q = int(request.POST.get("qty"))
			t = p.price

			try:
				c = models.Cart.objects.get(product = p, user = request.user) 	
				c.quantity += q
				c.total += q*t
				c.save()

			except:
				new_cart_i = models.Cart(user = request.user,
										product = p,
										quantity = q,
										price_per_item = t,
										total = q*t)
				
				new_cart_i.save()

			
			return HttpResponse(status = 204)
			
		except Exception as e:
			print(e)

class Cart(LoginRequiredMixin, ListView):	

	def get_login_url(self):
		return "/auth/login"

	def get(self, request):
		try:
			items = models.Cart.objects.filter(user = request.user)
			data = None
			total = 0
			if len(items) > 0:
				data = []
				for i, j in enumerate(items):
					data.append((i+1, j))
					total += j.total

			context = {"data": data, "page": "My Cart", "total": total}
			return render(request, "pages/cart.html", context) 

		except Exception as e:
			print(e)
			return HttpResponseServerError("Some error occured! Please try again!")

	def post(self, request):
		try:
			# items = models.Cart.objects.filter(user = request.user)
			key = request.POST.get("key")
			amount = 0
			if key:
				items = [models.Cart.objects.get(id = key)]
			else:
				items = models.Cart.objects.all()

			new_orders = []
			for i in items:
				# models.Order.objects.create(user = request.user, 
				# 							product = i.product,
				# 							quantity = i.quantity, 
				# 							total_amount = i.quantity * i.price_per_item)
				new_orders.append(models.Order(user = request.user, 
												product = i.product,
												quantity = i.quantity, 
												total_amount = i.total))
				amount += i.total

			for o in new_orders:
				o.save()
			
			for i in items:
				models.Cart.objects.get(id = i.id).delete()	
			

			return render(request, "/pages/payment.html", {"amount": amount})

		except Exception as e:
			print(e)
			return HttpResponseServerError("Some Error Occured! Please try again!")


class RemoveFromCart(LoginRequiredMixin, View):
	def get_login_url(self):
		return "/auth/login"

	def post(self, request, pk):
		try:
			models.Cart.objects.get(id = pk).delete()
			return HttpResponse(status = 204)
		except Exception as e:
			print(e)
			return HttpResponseBadRequest("Some Error Occured! Please try again!")

class EmptyCart(LoginRequiredMixin, View):
	def get_login_url(self):
		return "/auth/login"

	def post(self, request):
		try:
			models.Cart.objects.filter(user = request.user).delete()
			return HttpResponse(status = 204)
		except Exception as e:
			print(e)
			return HttpResponseBadRequest("Some Error Occured! Please try again!")


class Payments(LoginRequiredMixin, View):
	def post(self, request):
		try:
			# if request.POST.exists("key"):
			# 	return render(request, "/pages/payment.html", {"item": models.Cart.objects.get(id = key)});
			# else:
			# 	amount = 0;
			# 	for i in models.Cart.objects.filter(user = request.user):
			# 		amount += i.total
			i = request.POST.get("key", None)
			
			if i:

				item = models.Cart.objects.get(id = int(i))
				context = {
					"page": "Make Online Payment",
					"id": item.id,
					"amount": item.total
				}
			
			else:

				context = {
					"page": "Make Online Payment",
					"id": None,
					"amount": models.Cart.objects.filter(user = request.user).aggregate(Sum("total"))["total__sum"]
				}

			return render(request, "pages/payment.html", context)	
			
		except Exception as e:
			print(e)
			return HttpResponseBadRequest("Some Error Occured in payment! Please try again!")			


class Order(LoginRequiredMixin, View):


	# Implement stock decrease!!!


	def get_login_url(self):
		return "/auth/login"

	def get(self, request):
		try:
			orders = models.Order.objects.filter(user = request.user)
			context = {"orders": [(i+1, j) for i, j in enumerate(orders)], "page": "My Orders"}

			return render(request, "pages/orders.html", context)

		except Exception as e:
			print(e)
			return HttpResponseServerError("Some Error Occured! Please try again!")

	def post(self, request):
		try:
			if request.POST.get("key"):
				keys = [models.Cart.objects.get(id = request.POST.get("key"))]
			else:
				keys = list(models.Cart.objects.filter(user = request.user))

			print(keys)

			try:
				for key in keys:
					ci = models.Cart.objects.get(id = key.id)
					p = ci.product

					o = models.Order(user = request.user, 
						product = ci.product, 
						quantity = ci.quantity, 
						total_amount = ci.total)
					o.save()
					print("o saved")
					p.stock = max(0, p.stock - ci.quantity)
					print("p stock saved")
					p.save()
					print("p saved")
					ci.delete()
					print("ci deleted")

				orders = models.Order.objects.filter(user = request.user)
				context = {"orders": [(i+1, j) for i, j in enumerate(orders)], "page": "My Orders"}

				return render(request, "pages/orders.html", context)
			except Exception as e:
				print(e)
				return HttpResponseServerError("Some Error Occured inside try! Please try again!")
				

		except Exception as e:
			print(e)
			return HttpResponseServerError("Some Error Occured outside! Please try again!")


	def delete(self, request):
		
		body = request.body.decode('utf-8')
		key = int(body[4:])

		try:
			o = models.Order.objects.get(id = key)
			o.status = "Cancelled"
			o.save()
			return HttpResponse(status = 204)
		except Exception as e:
			print(e)
			return HttpResponseServerError("Some Error Occured outside! Please try again!")

	