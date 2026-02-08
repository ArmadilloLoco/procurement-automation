import yaml
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from accounts.models import User
from products.models import Supplier, Product, ProductAttribute

User = get_user_model()

class Command(BaseCommand):
    help = 'Импорт товаров из YAML-файла'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Путь к YAML-файлу')

    def handle(self, *args, **options):
        file_path = options['file_path']
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except FileNotFoundError:
            self.stderr.write(f"Файл не найден: {file_path}")
            return
        except yaml.YAMLError as e:
            self.stderr.write(f"Ошибка YAML: {e}")
            return

        supplier_info = data.get('supplier')
        products = data.get('products', [])

        if not supplier_info or not products:
            self.stderr.write("Ошибка: в файле должны быть 'supplier' и 'products'")
            return

        # --- Создание или получение поставщика ---
        company_name = supplier_info['company_name']
        supplier_email = supplier_info.get('email', f"{company_name.replace(' ', '_').lower()}@example.com")

        # Получаем или создаём пользователя-поставщика
        supplier_user, user_created = User.objects.get_or_create(
            email=supplier_email,
            defaults={
                'username': supplier_email.split('@')[0],
                'is_supplier': True,
                'password': 'pass123'
            }
        )
        if user_created:
            # Устанавливаем безопасный пароль
            supplier_user.set_unusable_password()
            supplier_user.save()

        # Получаем или создаём запись Supplier
        supplier, _ = Supplier.objects.get_or_create(
            user=supplier_user,
            defaults={'company_name': company_name}
        )
        supplier.accepts_orders = supplier_info.get('accepts_orders', True)
        supplier.save()

        # --- Импорт товаров ---
        created_count = 0
        with transaction.atomic():
            for prod in products:
                product, prod_created = Product.objects.get_or_create(
                    name=prod['name'],
                    supplier=supplier,
                    defaults={
                        'price': prod['price'],
                        'description': prod.get('description', '')
                    }
                )
                if prod_created:
                    created_count += 1

                # Обновляем цену и описание, если товар уже существует
                if not prod_created:
                    product.price = prod['price']
                    product.description = prod.get('description', '')
                    product.save()

                # Удаляем старые атрибуты и добавляем новые (простой способ)
                product.attributes.all().delete()
                for attr in prod.get('attributes', []):
                    ProductAttribute.objects.create(
                        product=product,
                        name=attr['name'],
                        value=attr['value']
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно импортировано {created_count} новых товаров от '{company_name}'"
            )
        )