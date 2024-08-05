# commission/services.py

from decimal import Decimal
from django.utils import timezone
from .models import MeetingSummary, Transaction, Product, CommissionStructure, Client
from .gateways import GroqGateway

def calculate_commission(transaction):
    commission_structures = CommissionStructure.objects.filter(
        agreement__agent=transaction.agent,
        product=transaction.product
    )
    commissions = []

    for structure in commission_structures:
        amount = Decimal(0)

        if structure.commission_type == 'SCOPE':
            # Example: Scope commission is a percentage of the transaction amount
            amount = Decimal(transaction.metadata.get('amount', 0)) * (structure.rate / Decimal(100))
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

            commission_data = {
                'transaction': transaction,
                'commission_structure': structure,
                'amount': amount,
                'expected_payment_date': expected_payment_date,
                'status': 'PENDING'
            }
            commissions.append(commission_data)

    return commissions

def process_meeting_summary(user, content):
    groq_gateway = GroqGateway()
    extracted_info = groq_gateway.extract_meeting_summary_info(content)
    
    # Add error handling for missing keys
    client_name = extracted_info.get('client_name')
    product_name = extracted_info.get('product_name')
    amount = extracted_info.get('amount')
    product_category = extracted_info.get('product_category', 'INSURANCE')

    if client_name and product_name and amount:
        # Create MeetingSummary
        summary = MeetingSummary.objects.create(
            agent=user,
            content=content,
            processed_status='SUCCESS'
        )
        
        # Create or get Product
        product, _ = Product.objects.get_or_create(
            name=product_name,
            defaults={'category': product_category}
        )
        
        # Create or get Client
        client, _ = Client.objects.get_or_create(
            display_name=client_name,
            defaults={'first_name': client_name.split()[0], 'last_name': client_name.split()[-1]}
        )
        
        # Create Transaction
        transaction = Transaction.objects.create(
            agent=user,
            client=client,
            product=product,
            metadata={'amount': amount}
        )
        
        return summary, transaction
    else:
        # Handle the case where required information is missing
        summary = MeetingSummary.objects.create(
            agent=user,
            content=content,
            processed_status='FAILED'
        )
        return summary, None