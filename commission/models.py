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
    type = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class ProductTransactionSchema(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transaction_schemas')
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=50)
    is_required = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - {self.field_name}"

class Agreement(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('EXPIRED', 'Expired'),
    ]
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    terms = models.JSONField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')

    def __str__(self):
        return f"Agreement between {self.agent.username} and {self.company.name}"

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

class CommissionStructure(models.Model):
    COMMISSION_TYPE_CHOICES = [
        ('SCOPE', 'Scope Commission'),
        ('RECURRING', 'Recurring Commission'),
        ('RETENTION', 'Retention Bonus'),
        ('OVERRIDE', 'Override Commission'),
        ('TRAIL', 'Trail Commission'),
        ('RENEWAL', 'Renewal Commission'),
    ]
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE, related_name='commission_structures')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    commission_type = models.CharField(max_length=20, choices=COMMISSION_TYPE_CHOICES)
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    payment_terms = models.ForeignKey(PaymentTerms, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_commission_type_display()} for {self.product.name}"

class Transaction(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=50)
    details = models.JSONField()

    def __str__(self):
        return f"Transaction for {self.client_name} - {self.product.name}"

class Commission(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    commission_structure = models.ForeignKey(CommissionStructure, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expected_payment_date = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Commission for {self.transaction}"

class MeetingSummary(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    content = models.TextField()
    processed_status = models.CharField(max_length=50)

    def __str__(self):
        return f"Meeting Summary for {self.agent.username} on {self.date}"