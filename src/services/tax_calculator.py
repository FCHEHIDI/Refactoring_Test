"""
Tax Calculator
Centralise les calculs de taxes dispersés dans le legacy.
"""

from typing import List, Dict
from ..models.order import Order
from ..models.product import Product
from ..config.constants import TAX_RATE


class TaxCalculator:
    """
    Calculateur de taxes.
    Responsabilité unique: calculer les taxes selon les produits taxables.
    """
    
    def __init__(self, tax_rate: float = TAX_RATE):
        """
        Args:
            tax_rate: Taux de taxe (défaut: 20%)
        """
        self.tax_rate = tax_rate
    
    def calculate(
        self,
        items: List[Order],
        products: Dict[str, Product],
        taxable_amount: float
    ) -> float:
        """
        Calcule la taxe selon si tous les produits sont taxables.
        
        Le legacy a 2 méthodes:
        - Si tous taxables: applique taux sur montant taxable global
        - Sinon: calcule ligne par ligne
        
        On préserve ce comportement.
        
        Args:
            items: Liste des commandes
            products: Dict des produits par ID
            taxable_amount: Montant taxable (après remises)
            
        Returns:
            Montant de la taxe arrondi à 2 décimales
        """
        if self._all_taxable(items, products):
            return round(taxable_amount * self.tax_rate, 2)
        
        return self._calculate_per_line(items, products)
    
    def _all_taxable(
        self,
        items: List[Order],
        products: Dict[str, Product]
    ) -> bool:
        """Vérifie si tous les produits de la commande sont taxables"""
        for item in items:
            prod = products.get(item.product_id)
            if prod and not prod.taxable:
                return False
        return True
    
    def _calculate_per_line(
        self,
        items: List[Order],
        products: Dict[str, Product]
    ) -> float:
        """Calcule la taxe ligne par ligne (pour commandes mixtes)"""
        tax = 0.0
        
        for item in items:
            prod = products.get(item.product_id)
            if prod and prod.taxable:
                item_total = item.qty * prod.price
                tax += item_total * self.tax_rate
        
        return round(tax, 2)
