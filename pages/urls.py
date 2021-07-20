from pages import views
from django.urls import path

urlpatterns = [
	path("products/all/", views.All_Products.as_view()),
	path("products/<int:pk>/", views.Specific_Product.as_view()),
	path("products/buy/<int:pk>", views.Buy_Product.as_view()),
	path("cart/", views.Cart.as_view()),
	path("cart/remove", views.EmptyCart.as_view()),
	path("cart/remove/<int:pk>", views.RemoveFromCart.as_view()),
	path("payment/", views.Payments.as_view(), name = "payment"),
	# path("payment/all", views.Payments_all.as_view())
	path("orders/", views.Order.as_view()),
	path("about", views.about),
	path("", views.index)
]