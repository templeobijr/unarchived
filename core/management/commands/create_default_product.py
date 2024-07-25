from django.core.management.base import BaseCommand
from core.models import BrandProfile, Product, CustomUser

class Command(BaseCommand):
    help = 'Create a default product for migration purposes'

    def handle(self, *args, **kwargs):
        user = CustomUser.objects.first()
        if not user:
            user = CustomUser.objects.create(username='defaultuser', password='defaultpass')

        brand, created = BrandProfile.objects.get_or_create(user=user, name='Default Brand', logo='', description='Default brand for migration')
        
        product, created = Product.objects.get_or_create(
            name='Default Product',
            description='Default product for migration',
            price=0.0,
            brand=brand,
            image=''
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully created default product with ID %s' % product.id))
