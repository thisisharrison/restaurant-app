from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Size(models.Model):
    S = 'Small'
    L = 'Large'
    size_choices = ((S, 'Small'), (L, 'Large'))
    size = models.CharField(
        max_length=8, choices=size_choices, default=S, null=True)

    def __str__(self):
        return f"{self.size}"


class Category(models.Model):
    pizza = 'Pizza'
    subs = 'Subs'
    pasta = 'Pasta'
    salads = 'Salads'
    platters = 'Dinner Platters'
    category_choices = ((pizza, 'pizza'), (subs, 'subs'),
                        (pasta, 'pasta'), (salads, 'salads'), (platters, 'platters'))
    name = models.CharField(
        max_length=64, choices=category_choices, default=pizza)

    def __str__(self):
        return self.name


class Crust(models.Model):
    regular = 'Regular'
    sicilian = 'Sicilian'
    crust_choices = [(regular, 'regular'),
                     (sicilian, 'sicilian')]
    crust = models.CharField(
        max_length=8, choices=crust_choices, blank=True, default=regular)

    def __str__(self):
        return self.crust


class MenuItem(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    size = models.ForeignKey(
        Size, on_delete=models.CASCADE, blank=True, null=True)
    crust = models.ForeignKey(
        Crust, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0.5)

    def __str__(self):
        return f"{self.name}, {self.category}, ${self.price}"


# Cart / Customized Item
class OrderItem(models.Model):
    zero = 0
    one = 1
    two = 2
    three = 3
    special = 4
    amount_choices = ((zero, '0'), (one, '1'), (two, '2'),
                      (three, '3'), (special, '4'))
    topping = models.ManyToManyField(
        Topping, blank=True, related_name="pizzas")
    amount = models.IntegerField(choices=amount_choices, default=zero)
    name = models.ForeignKey(MenuItem, null=True, on_delete=models.SET_NULL)
    price = models.FloatField(default=0.5)

    def __str__(self):
        return f"{self.name} {self.topping.all()} {self.amount}"


class Order(models.Model):
    pending = 'PEND'
    confirmed = 'CONF'
    preparing = 'PREP'
    ready = 'READ'
    shipped = 'SHIP'
    status_choices = [(pending, 'pending'), (confirmed, 'confirmed'),
                      (preparing, 'preparing'), (ready, 'ready'), (shipped, 'shipped')]
    username = models.ForeignKey(
        User, on_delete=models.CASCADE)
    item_order = models.ForeignKey(
        OrderItem, null=True, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(auto_now_add=True)
    shipped_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=4, choices=status_choices, default=pending)
    shipping = models.BooleanField(default=False)

    def __str__(self):
        return f"Customer: {self.username}, Order ID: {self.id}, Status: {self.status}, Ordered: {self.ordered_date}, Item: {self.item_order}, {self.item_order.topping.values()}"
