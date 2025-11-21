"""
Order Repository
Gère le chargement des commandes depuis CSV.
"""

from pathlib import Path
from typing import List
from .csv_repository import CSVRepository
from ..models.order import Order


class OrderRepository:
    """Repository pour charger les commandes depuis orders.csv"""
    
    def __init__(self):
        self.repo = CSVRepository(self._map_order)
    
    def _map_order(self, row: dict) -> Order:
        """
        Transforme une ligne CSV en objet Order.
        
        Préserve le comportement legacy:
        - Validation qty > 0 et price >= 0
        - Valeurs par défaut pour champs optionnels
        - Skip silencieux si validation échoue (ValueError propagée au CSVRepository)
        """
        qty = int(row['qty'])
        unit_price = float(row['unit_price'])
        
        # Validation legacy: skip si invalide (exception propagée)
        if qty <= 0 or unit_price < 0:
            raise ValueError(f"Invalid order: qty={qty}, price={unit_price}")
        
        return Order(
            id=row['id'],
            customer_id=row['customer_id'],
            product_id=row['product_id'],
            qty=qty,
            unit_price=unit_price,
            date=row.get('date', ''),
            promo_code=row.get('promo_code', ''),
            time=row.get('time', '12:00')
        )
    
    def load_all(self, file_path: Path | str) -> List[Order]:
        """
        Charge toutes les commandes.
        
        Args:
            file_path: Chemin vers orders.csv
            
        Returns:
            List[Order]
        """
        return self.repo.load(file_path)
