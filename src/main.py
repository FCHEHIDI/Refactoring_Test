"""
Main Entry Point - Refactored Order Report Generator

Architecture propre basée sur la séparation des responsabilités:
1. Repositories: Chargement des données (I/O)
2. Services: Logique métier (pure functions)
3. Formatters: Présentation (pure functions)
4. Main: Orchestration simple

Remplace la god function de 280+ lignes du legacy.
"""

from pathlib import Path
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Repositories (I/O layer)
from src.repositories.customer_repository import CustomerRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.order_repository import OrderRepository
from src.repositories.promotion_repository import PromotionRepository
from src.repositories.shipping_zone_repository import ShippingZoneRepository

# Services (Business logic)
from src.services.order_processor import OrderProcessor

# Formatters (Presentation)
from src.formatters.text_formatter import TextReportFormatter


def main() -> str:
    """
    Point d'entrée principal.
    Architecture claire en 5 étapes:
    1. Configuration des chemins
    2. Chargement des données (repositories)
    3. Traitement métier (services)
    4. Formatage (formatters)
    5. Output (I/O)
    
    Returns:
        Le rapport texte généré
    """
    # 1. Configuration
    base_path = Path(__file__).parent.parent / 'legacy' / 'data'
    
    # 2. Chargement des données (séparation I/O)
    customers = CustomerRepository().load_all(base_path / 'customers.csv')
    products = ProductRepository().load_all(base_path / 'products.csv')
    orders = OrderRepository().load_all(base_path / 'orders.csv')
    promotions = PromotionRepository().load_all(base_path / 'promotions.csv')
    shipping_zones = ShippingZoneRepository().load_all(base_path / 'shipping_zones.csv')
    
    # 3. Traitement métier (logique pure)
    processor = OrderProcessor()
    summaries = []
    
    # Grouper les commandes par client et traiter
    # Tri par ID client pour ordre déterministe (comportement legacy)
    for customer_id in sorted(customers.keys()):
        customer = customers[customer_id]
        
        # Filtrer les commandes de ce client
        customer_orders = [o for o in orders if o.customer_id == customer_id]
        
        if not customer_orders:
            continue  # Skip clients sans commandes
        
        # Traiter les commandes du client
        summary = processor.process_customer_orders(
            customer=customer,
            orders=customer_orders,
            products=products,
            promotions=promotions,
            shipping_zones=shipping_zones
        )
        
        summaries.append(summary)
    
    # 4. Formatage (présentation)
    formatter = TextReportFormatter()
    report = formatter.format(summaries)
    
    # 5. Output (I/O isolé)
    print(report)
    
    return report


if __name__ == '__main__':
    main()
