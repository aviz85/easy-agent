from django.core.management.base import BaseCommand
from commission.models import CommissionStructure, Agreement

class Command(BaseCommand):
    help = 'Fills empty agent and agreement fields in CommissionStructure'

    def handle(self, *args, **options):
        for cs in CommissionStructure.objects.filter(agent__isnull=True):
            # Try to find a matching agreement
            agreement = Agreement.objects.filter(agent=cs.agent, company__product=cs.product).first()
            if agreement:
                cs.agreement = agreement
                cs.save()
            else:
                self.stdout.write(self.style.WARNING(f'No matching agreement found for CommissionStructure {cs.id}'))
        
        # Fill agent field based on agreement
        for cs in CommissionStructure.objects.filter(agent__isnull=True, agreement__isnull=False):
            cs.agent = cs.agreement.agent
            cs.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully filled agent and agreement fields'))