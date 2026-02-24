from django.test import TestCase
from shoes_market.models import Product, MeasureUnit, Supplier, Producer, Category

class ProductDiscountPriceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаём минимально необходимые связанные объекты
        cls.unit = MeasureUnit.objects.create(name='шт')
        cls.supplier = Supplier.objects.create(name='Test Supplier')
        cls.producer = Producer.objects.create(name='Test Producer')
        cls.category = Category.objects.create(name='Test Category')

    def test_discount_price_calculation(self):
        """Проверяем корректность расчёта цены со скидкой."""
        product = Product.objects.create(
            article='ART123',
            name='Test Product',
            measure_unit=self.unit,
            price=1000,
            supplier=self.supplier,
            producer=self.producer,
            category=self.category,
            discount=15,
            quantity=10,
            description='Test description'
        )
        expected_price = round(1000 - 1000 * 15 * 0.01, 2)  # 850.0
        self.assertEqual(product.discount_price(), expected_price)

        # Проверка с другой скидкой и ценой
        product.discount = 25
        product.price = 2000
        expected_price = round(2000 - 2000 * 25 * 0.01, 2)  # 1500.0
        self.assertEqual(product.discount_price(), expected_price)
