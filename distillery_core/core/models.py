from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    batch_type = models.CharField(max_length=100)
    ingredients = models.JSONField()
    process_steps = models.TextField()
    abv_target = models.FloatField(default=0.0)
    fermentation_temp = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Batch(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='In Progress')

class Vessel(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    capacity = models.FloatField()
    occupied = models.BooleanField(default=False)

class Inventory(models.Model):
    item = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    quantity = models.FloatField()
    barcode = models.CharField(max_length=100, unique=True)

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)

class Customer(models.Model):
    name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)

class PurchaseOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class Timesheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.FloatField()
    task = models.CharField(max_length=200)