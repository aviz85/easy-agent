# commission/services.py

from decimal import Decimal
from django.utils import timezone
from .models import MeetingSummary, Transaction, Product, CommissionStructure, Commission
from .gateways import GroqGateway

def calculate_commission(transaction):
    commissions = []
    commission_structures = CommissionStructure.objects.filter(
        agreement__agent=transaction.agent,
        product=transaction.product
    )

    for structure in commission_structures:
        amount = Decimal(0)

        if structure.commission_type == 'SCOPE':
            # Example: Scope commission is a percentage of the transaction amount
            amount = Decimal(transaction.details.get('amount', 0)) * (structure.rate / Decimal(100))
        elif structure.commission_type == 'RECURRING':
            # Example: Recurring commission is a fixed amount
            amount = structure.rate
        # Add more commission type calculations as needed

        if amount > 0:
            # Calculate expected payment date based on payment terms
            if structure.payment_terms.payment_type == 'DAY_OF_MONTH':
                current_date = timezone.now().date()
                if current_date.day <= structure.payment_terms.day_of_month:
                    expected_payment_date = current_date.replace(day=structure.payment_terms.day_of_month)
                else:
                    next_month = current_date.replace(day=28) + timezone.timedelta(days=4)
                    expected_payment_date = next_month.replace(day=structure.payment_terms.day_of_month)
            else:  # SPECIFIC_DATE
                expected_payment_date = structure.payment_terms.specific_date
                if expected_payment_date < timezone.now().date():
                    expected_payment_date = expected_payment_date.replace(year=expected_payment_date.year + 1)

            commission = Commission.objects.create(
                transaction=transaction,
                commission_structure=structure,
                amount=amount,
                expected_payment_date=expected_payment_date,
                status='PENDING'
            )
            commissions.append(commission)

    return commissions

def process_meeting_summary(user, content):
    groq_gateway = GroqGateway()
    extracted_info = groq_gateway.extract_meeting_summary_info(content)
    
    # Add error handling for missing keys
    client_name = extracted_info.get('client_name')
    product_name = extracted_info.get('product_name')
    amount = extracted_info.get('amount')
    product_type = extracted_info.get('product_type')  # Add this line

    if client_name and product_name and amount:
        # Create MeetingSummary
        summary = MeetingSummary.objects.create(
            agent=user,
            date=timezone.now().date(),
            content=content,
            processed_status='SUCCESS'
        )
        
        # Create Transaction
        product, _ = Product.objects.get_or_create(
            name=product_name,
            defaults={
                'category': extracted_info.get('product_category', 'INSURANCE'),
                'type': product_type  # Add this line
            }
        )
        
        # Update the product type if it's a new value
        if product.type != product_type:
            product.type = product_type
            product.save()
        
        transaction = Transaction.objects.create(
            agent=user,
            client_name=client_name,
            product=product,
            date=timezone.now().date(),
            status='PENDING',
            details={'amount': amount}
        )
        
        return summary, transaction
    else:
        # Handle the case where required information is missing
        summary = MeetingSummary.objects.create(
            agent=user,
            date=timezone.now().date(),
            content=content,
            processed_status='FAILED'
        )
        return summary, None