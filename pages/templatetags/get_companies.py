from django import template
from pages.models import Company
register = template.Library()

@register.simple_tag
def get_companies():
	companies = Company.objects.all()
	return companies