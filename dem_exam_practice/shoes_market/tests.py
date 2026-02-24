from django.test import TestCase
from .models import Product, MeasureUnit, Supplier, Producer, Category
from .views import get_filtered_products


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


class ProductSearchFilterTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаём тестовые данные
        unit = MeasureUnit.objects.create(name='шт')
        supplier1 = Supplier.objects.create(name='Adidas')
        supplier2 = Supplier.objects.create(name='Nike')
        producer = Producer.objects.create(name='Factory')
        category = Category.objects.create(name='Обувь')

        # Товары
        Product.objects.create(article='1', name='Кроссовки Adidas', measure_unit=unit,
                               price=100, supplier=supplier1, producer=producer,
                               category=category, discount=0, quantity=10,
                               description='Беговые')
        Product.objects.create(article='2', name='Футболка Nike', measure_unit=unit,
                               price=50, supplier=supplier2, producer=producer,
                               category=category, discount=0, quantity=5,
                               description='Спортивная')
        Product.objects.create(article='3', name='Кроссовки Nike', measure_unit=unit,
                               price=120, supplier=supplier2, producer=producer,
                               category=category, discount=0, quantity=15,
                               description='Для баскетбола')

    def test_filter_by_supplier(self):
        products = get_filtered_products(search_query='', quantity_sorting='', supplier_filter='2')  # Nike
        self.assertEqual(products.count(), 2)
        self.assertSetEqual(set(products.values_list('article', flat=True)), {'2', '3'})

    def test_search_by_name(self):
        products = get_filtered_products(search_query='Кроссовки', quantity_sorting='', supplier_filter='')
        self.assertEqual(products.count(), 2)  # товары 1 и 3
        self.assertSetEqual(set(products.values_list('article', flat=True)), {'1', '3'})

    def test_sort_by_quantity_asc(self):
        products = get_filtered_products(search_query='', quantity_sorting='asc', supplier_filter='')
        self.assertEqual(list(products.values_list('quantity', flat=True)), [5, 10, 15])