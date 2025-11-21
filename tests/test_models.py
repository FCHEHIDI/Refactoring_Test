"""
Tests unitaires pour les Models
Vérifie l'encapsulation, la validation et les comportements des entités.
"""

import pytest
from src.models.customer import Customer
from src.models.product import Product
from src.models.order import Order
from src.models.promotion import Promotion
from src.models.shipping_zone import ShippingZone
from src.models.order_summary import OrderSummary


class TestCustomer:
    """Tests du modèle Customer"""
    
    def test_customer_creation_basic(self):
        """Test création client avec valeurs par défaut"""
        customer = Customer(id='C001', name='Alice Martin')
        
        assert customer.id == 'C001'
        assert customer.name == 'Alice Martin'
        assert customer.level == 'BASIC'
        assert customer.shipping_zone == 'ZONE1'
        assert customer.currency == 'EUR'
    
    def test_customer_creation_premium(self):
        """Test création client premium"""
        customer = Customer(
            id='C002',
            name='Bob Durant',
            level='PREMIUM',
            shipping_zone='ZONE2',
            currency='USD'
        )
        
        assert customer.level == 'PREMIUM'
        assert customer.is_premium()
        assert not customer.is_vip()
    
    def test_customer_is_vip(self):
        """Test méthode is_vip()"""
        vip = Customer(id='C003', name='VIP Client', level='VIP')
        assert vip.is_vip()
        assert vip.is_premium()  # VIP est aussi premium
    
    def test_customer_immutability(self):
        """Test que Customer est immutable (frozen)"""
        customer = Customer(id='C001', name='Alice')
        
        with pytest.raises(AttributeError):
            customer.name = 'Bob'


class TestProduct:
    """Tests du modèle Product"""
    
    def test_product_creation(self):
        """Test création produit normal"""
        product = Product(
            id='P001',
            name='Laptop',
            category='Electronics',
            price=999.99,
            weight=2.5,
            taxable=True
        )
        
        assert product.id == 'P001'
        assert product.name == 'Laptop'
        assert product.price == 999.99
        assert product.weight == 2.5
        assert product.taxable is True
    
    def test_product_default_values(self):
        """Test valeurs par défaut"""
        product = Product(
            id='P002',
            name='Book',
            category='Books',
            price=15.99
        )
        
        assert product.weight == 1.0
        assert product.taxable is True
    
    def test_product_negative_price_validation(self):
        """Test validation prix négatif"""
        with pytest.raises(ValueError, match="prix ne peut pas être négatif"):
            Product(
                id='P003',
                name='Invalid',
                category='Test',
                price=-10.0
            )
    
    def test_product_negative_weight_validation(self):
        """Test validation poids négatif"""
        with pytest.raises(ValueError, match="poids ne peut pas être négatif"):
            Product(
                id='P004',
                name='Invalid',
                category='Test',
                price=10.0,
                weight=-5.0
            )


class TestOrder:
    """Tests du modèle Order"""
    
    def test_order_creation(self):
        """Test création commande"""
        order = Order(
            id='O001',
            customer_id='C001',
            product_id='P001',
            qty=2,
            unit_price=50.0,
            date='2024-01-15',
            promo_code='PROMO10',
            time='09:30'
        )
        
        assert order.id == 'O001'
        assert order.qty == 2
        assert order.unit_price == 50.0
        assert order.get_hour() == 9
        assert order.line_total() == 100.0
    
    def test_order_default_values(self):
        """Test valeurs par défaut"""
        order = Order(
            id='O002',
            customer_id='C001',
            product_id='P001',
            qty=1,
            unit_price=25.0
        )
        
        assert order.date == ''
        assert order.promo_code == ''
        assert order.time == '12:00'
        assert order.get_hour() == 12
    
    def test_order_zero_qty_validation(self):
        """Test validation quantité nulle"""
        with pytest.raises(ValueError, match="quantité doit être positive"):
            Order(
                id='O003',
                customer_id='C001',
                product_id='P001',
                qty=0,
                unit_price=50.0
            )
    
    def test_order_negative_price_validation(self):
        """Test validation prix négatif"""
        with pytest.raises(ValueError, match="prix unitaire ne peut pas être négatif"):
            Order(
                id='O004',
                customer_id='C001',
                product_id='P001',
                qty=1,
                unit_price=-10.0
            )
    
    def test_order_get_hour_invalid_time(self):
        """Test extraction heure avec format invalide"""
        order = Order(
            id='O005',
            customer_id='C001',
            product_id='P001',
            qty=1,
            unit_price=10.0,
            time='invalid'
        )
        
        assert order.get_hour() == 12  # Défaut si invalide


class TestPromotion:
    """Tests du modèle Promotion"""
    
    def test_promotion_percentage(self):
        """Test promotion pourcentage"""
        promo = Promotion(
            code='PROMO10',
            type='PERCENTAGE',
            value=10.0,
            active=True
        )
        
        assert promo.get_discount_rate() == 0.1
        assert promo.get_fixed_discount() == 0.0
    
    def test_promotion_fixed(self):
        """Test promotion montant fixe"""
        promo = Promotion(
            code='FIXED50',
            type='FIXED',
            value=50.0
        )
        
        assert promo.get_discount_rate() == 0.0
        assert promo.get_fixed_discount() == 50.0
    
    def test_promotion_inactive(self):
        """Test promotion inactive"""
        promo = Promotion(
            code='OLD',
            type='PERCENTAGE',
            value=20.0,
            active=False
        )
        
        assert not promo.active


class TestShippingZone:
    """Tests du modèle ShippingZone"""
    
    def test_shipping_zone_creation(self):
        """Test création zone de livraison"""
        zone = ShippingZone(
            zone='ZONE1',
            base=5.0,
            per_kg=0.5
        )
        
        assert zone.zone == 'ZONE1'
        assert zone.base == 5.0
        assert zone.per_kg == 0.5
    
    def test_shipping_zone_default_per_kg(self):
        """Test valeur par défaut per_kg"""
        zone = ShippingZone(zone='ZONE2', base=8.0)
        assert zone.per_kg == 0.5
    
    def test_shipping_zone_negative_base_validation(self):
        """Test validation tarif de base négatif"""
        with pytest.raises(ValueError, match="tarif de base ne peut pas être négatif"):
            ShippingZone(zone='ZONE3', base=-5.0)
    
    def test_shipping_zone_negative_per_kg_validation(self):
        """Test validation tarif par kg négatif"""
        with pytest.raises(ValueError, match="tarif par kg ne peut pas être négatif"):
            ShippingZone(zone='ZONE4', base=5.0, per_kg=-1.0)


class TestOrderSummary:
    """Tests du modèle OrderSummary"""
    
    def test_order_summary_creation(self):
        """Test création résumé de commande"""
        customer = Customer(id='C001', name='Alice')
        
        summary = OrderSummary(
            customer=customer,
            subtotal=100.0,
            volume_discount=10.0,
            loyalty_discount=5.0,
            tax=17.0,
            shipping=5.0,
            handling=2.5,
            total=109.5,
            loyalty_points=120.0,
            weight=5.0,
            morning_bonus=3.0,
            item_count=3
        )
        
        assert summary.customer.id == 'C001'
        assert summary.subtotal == 100.0
        assert summary.total_discount == 15.0  # 10 + 5
        assert summary.taxable_amount == 85.0  # 100 - 15
        assert summary.morning_bonus == 3.0
        assert summary.item_count == 3
    
    def test_order_summary_default_values(self):
        """Test valeurs par défaut"""
        customer = Customer(id='C002', name='Bob')
        
        summary = OrderSummary(
            customer=customer,
            subtotal=50.0,
            volume_discount=0.0,
            loyalty_discount=0.0,
            tax=10.0,
            shipping=0.0,
            handling=0.0,
            total=60.0,
            loyalty_points=0.0,
            weight=1.0
        )
        
        assert summary.morning_bonus == 0.0
        assert summary.item_count == 0
