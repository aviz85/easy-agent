# commission/models.py

from django.db import models
from django.contrib.auth.models import User

class InsuranceCompany(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('INSURANCE', 'Insurance'),
        ('PENSION', 'Pension'),
        ('FINANCIAL', 'Financial'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class PaymentTerms(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('DAY_OF_MONTH', 'Day of Month'),
        ('SPECIFIC_DATE', 'Specific Date'),
    ]
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    day_of_month = models.IntegerField(null=True, blank=True)
    specific_date = models.DateField(null=True, blank=True)

    def __str__(self):
        if self.payment_type == 'DAY_OF_MONTH':
            return f"Day {self.day_of_month} of each month"
        return f"Annually on {self.specific_date}"

class Agreement(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Agreement between {self.agent.username} and {self.company.name}"

class CommissionStructure(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    commission_type = models.CharField(max_length=20, choices=[('SCOPE', 'Scope'), ('RECURRING', 'Recurring')])
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    payment_terms = models.ForeignKey(PaymentTerms, on_delete=models.CASCADE)
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.agent.username} - {self.product.name} - {self.commission_type}"

class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name

class Transaction(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey('commission.Client', on_delete=models.PROTECT, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)

    def __str__(self):
        return f"Transaction for {self.client.display_name} - {self.product.name}"

class MeetingSummary(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    processed_status = models.CharField(max_length=50)

    def __str__(self):
        return f"Meeting Summary for {self.agent.username} on {self.created_at.date()}"