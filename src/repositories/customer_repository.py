"""
Customer Repository
Gère le chargement des données clients depuis CSV.
"""

from pathlib import Path
from typing import Dict
from .csv_repository import CSVRepository
from ..models.customer import Customer


class CustomerRepository:
    """Repository pour charger les clients depuis customers.csv"""
    
    def __init__(self):
        self.repo = CSVRepository(self._map_customer)
    
    def _map_customer(self, row: Dict[str, str]) -> Customer:
        """
        Transforme une ligne CSV en objet Customer.
        
        Préserve le comportement legacy:
        - Valeurs par défaut si colonnes manquantes
        - Pas d'exception si données incomplètes
        """
        return Customer(
            id=row['id'],
            name=row['name'],
            level=row.get('level', 'BASIC'),
            shipping_zone=row.get('shipping_zone', 'ZONE1'),
            currency=row.get('currency', 'EUR')
        )
    
    def load_all(self, file_path: Path | str) -> Dict[str, Customer]:
        """
        Charge tous les clients et retourne un dict indexé par ID.
        
        Args:
            file_path: Chemin vers customers.csv
            
        Returns:
            Dict[customer_id, Customer]
        """
        return self.repo.load_as_dict(file_path, 'id')
