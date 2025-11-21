"""
Tests unitaires pour les Repositories
Vérifie le chargement des données CSV en objets typés.
"""

import pytest
from pathlib import Path
from src.repositories.customer_repository import CustomerRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.order_repository import OrderRepository
from src.repositories.promotion_repository import PromotionRepository
from src.repositories.shipping_zone_repository import ShippingZoneRepository


# Chemin vers les données de test (legacy data)
DATA_PATH = Path(__file__).parent.parent / 'legacy' / 'data'


class TestCustomerRepository:
    """Tests du CustomerRepository"""
    
    def test_load_customers(self):
        """Test chargement de tous les clients"""
        repo = CustomerRepository()
        customers = repo.load_all(DATA_PATH / 'customers.csv')
        
        # Vérifier qu'on a chargé des clients
        assert len(customers) > 0
        
        # Vérifier la structure (dict indexé par ID)
        assert 'C001' in customers or 'C002' in customers
        
        # Vérifier qu'on a des objets Customer
        first_customer = next(iter(customers.values()))
        assert hasattr(first_customer, 'id')
        assert hasattr(first_customer, 'name')
        assert hasattr(first_customer, 'level')
    
    def test_customer_default_values(self):
        """Test que les valeurs par défaut sont appliquées"""
        repo = CustomerRepository()
        customers = repo.load_all(DATA_PATH / 'customers.csv')
        
        # Au moins un client devrait avoir les valeurs par défaut ou explicites
        for customer in customers.values():
            assert customer.level in ('BASIC', 'PREMIUM', 'VIP')
            assert customer.currency in ('EUR', 'USD', 'GBP')
            assert customer.shipping_zone.startswith('ZONE')


class TestProductRepository:
    """Tests du ProductRepository"""
    
    def test_load_products(self):
        """Test chargement de tous les produits"""
        repo = ProductRepository()
        products = repo.load_all(DATA_PATH / 'products.csv')
        
        assert len(products) > 0
        
        # Vérifier qu'on a des objets Product
        first_product = next(iter(products.values()))
        assert hasattr(first_product, 'id')
        assert hasattr(first_product, 'name')
        assert hasattr(first_product, 'price')
        assert hasattr(first_product, 'weight')
        assert hasattr(first_product, 'taxable')
    
    def test_product_types(self):
        """Test que les types sont correctement convertis"""
        repo = ProductRepository()
        products = repo.load_all(DATA_PATH / 'products.csv')
        
        for product in products.values():
            assert isinstance(product.price, float)
            assert isinstance(product.weight, float)
            assert isinstance(product.taxable, bool)
            assert product.price >= 0
            assert product.weight > 0


class TestOrderRepository:
    """Tests du OrderRepository"""
    
    def test_load_orders(self):
        """Test chargement de toutes les commandes"""
        repo = OrderRepository()
        orders = repo.load_all(DATA_PATH / 'orders.csv')
        
        assert len(orders) > 0
        
        # Vérifier qu'on a des objets Order
        first_order = orders[0]
        assert hasattr(first_order, 'id')
        assert hasattr(first_order, 'customer_id')
        assert hasattr(first_order, 'product_id')
        assert hasattr(first_order, 'qty')
        assert hasattr(first_order, 'unit_price')
    
    def test_order_validation(self):
        """Test que les commandes invalides sont filtrées (qty <= 0)"""
        repo = OrderRepository()
        orders = repo.load_all(DATA_PATH / 'orders.csv')
        
        # Toutes les commandes chargées doivent être valides
        for order in orders:
            assert order.qty > 0
            assert order.unit_price >= 0
    
    def test_order_types(self):
        """Test que les types sont correctement convertis"""
        repo = OrderRepository()
        orders = repo.load_all(DATA_PATH / 'orders.csv')
        
        for order in orders:
            assert isinstance(order.qty, int)
            assert isinstance(order.unit_price, float)


class TestPromotionRepository:
    """Tests du PromotionRepository"""
    
    def test_load_promotions(self):
        """Test chargement des promotions"""
        repo = PromotionRepository()
        promotions = repo.load_all(DATA_PATH / 'promotions.csv')
        
        # Peut être vide si fichier manquant (comportement legacy)
        assert isinstance(promotions, dict)
        
        if len(promotions) > 0:
            first_promo = next(iter(promotions.values()))
            assert hasattr(first_promo, 'code')
            assert hasattr(first_promo, 'type')
            assert hasattr(first_promo, 'value')
            assert hasattr(first_promo, 'active')
    
    def test_promotion_types(self):
        """Test types de promotions"""
        repo = PromotionRepository()
        promotions = repo.load_all(DATA_PATH / 'promotions.csv')
        
        for promo in promotions.values():
            assert promo.type in ('PERCENTAGE', 'FIXED')
            assert isinstance(promo.value, float)
            assert isinstance(promo.active, bool)
    
    def test_missing_file_returns_empty_dict(self):
        """Test que fichier manquant retourne dict vide (comportement legacy)"""
        repo = PromotionRepository()
        promotions = repo.load_all(Path('/nonexistent/promotions.csv'))
        
        assert promotions == {}


class TestShippingZoneRepository:
    """Tests du ShippingZoneRepository"""
    
    def test_load_shipping_zones(self):
        """Test chargement des zones de livraison"""
        repo = ShippingZoneRepository()
        zones = repo.load_all(DATA_PATH / 'shipping_zones.csv')
        
        assert len(zones) > 0
        
        # Vérifier qu'on a des objets ShippingZone
        first_zone = next(iter(zones.values()))
        assert hasattr(first_zone, 'zone')
        assert hasattr(first_zone, 'base')
        assert hasattr(first_zone, 'per_kg')
    
    def test_shipping_zone_types(self):
        """Test que les types sont correctement convertis"""
        repo = ShippingZoneRepository()
        zones = repo.load_all(DATA_PATH / 'shipping_zones.csv')
        
        for zone in zones.values():
            assert isinstance(zone.base, float)
            assert isinstance(zone.per_kg, float)
            assert zone.base >= 0
            assert zone.per_kg >= 0


class TestIntegrationLoadAll:
    """Tests d'intégration: charger toutes les données ensemble"""
    
    def test_load_all_data(self):
        """Test qu'on peut charger toutes les données sans erreur"""
        customers = CustomerRepository().load_all(DATA_PATH / 'customers.csv')
        products = ProductRepository().load_all(DATA_PATH / 'products.csv')
        orders = OrderRepository().load_all(DATA_PATH / 'orders.csv')
        promotions = PromotionRepository().load_all(DATA_PATH / 'promotions.csv')
        zones = ShippingZoneRepository().load_all(DATA_PATH / 'shipping_zones.csv')
        
        # Vérifier qu'on a des données
        assert len(customers) > 0
        assert len(products) > 0
        assert len(orders) > 0
        assert len(zones) > 0
        # promotions peut être vide
        
        print(f"\nDonnées chargées:")
        print(f"  - {len(customers)} clients")
        print(f"  - {len(products)} produits")
        print(f"  - {len(orders)} commandes")
        print(f"  - {len(promotions)} promotions")
        print(f"  - {len(zones)} zones de livraison")
    
    def test_referential_integrity(self):
        """Test que les références entre entités sont cohérentes"""
        customers = CustomerRepository().load_all(DATA_PATH / 'customers.csv')
        products = ProductRepository().load_all(DATA_PATH / 'products.csv')
        orders = OrderRepository().load_all(DATA_PATH / 'orders.csv')
        
        # Toutes les commandes doivent référencer des clients et produits existants
        for order in orders:
            assert order.customer_id in customers, \
                f"Order {order.id} référence un client inexistant: {order.customer_id}"
            assert order.product_id in products, \
                f"Order {order.id} référence un produit inexistant: {order.product_id}"
