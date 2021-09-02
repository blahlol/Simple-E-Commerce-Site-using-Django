from django import template
from store.models import Category

register = template.Library()

def multiply(num1, num2):
    return int(num1) * int(num2)

def categories(str):
    return Category.objects.filter(meant_for = str)

def meant_for(dummy_str):
    return ['Men', 'Women', 'Boys', 'Girls']



register.filter('multiply', multiply)
register.filter('categories', categories)
register.filter('meant_for', meant_for)