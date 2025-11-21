"""
Product Repository
Gère le chargement des données produits depuis CSV.
"""

from pathlib import Path
from typing import Dict
from .csv_repository import CSVRepository
from ..models.product import Product


class ProductRepository:
    """Repository pour charger les produits depuis products.csv"""
    
    def __init__(self):
        self.repo = CSVRepository(self._map_product)
    
    def _map_product(self, row: Dict[str, str]) -> Product:
        """
        Transforme une ligne CSV en objet Product.
        
        Préserve le comportement legacy:
        - Valeurs par défaut si colonnes manquantes
        - Conversion des types (float, bool)
        - Skip silencieux si erreur (via le try/catch du CSVRepository)
        """
        return Product(
            id=row['id'],
            name=row['name'],
            category=row['category'],
            price=float(row['price']),
            weight=float(row.get('weight', '1.0')),
            taxable=row.get('taxable', 'true').lower() == 'true'
        )
    
    def load_all(self, file_path: Path | str) -> Dict[str, Product]:
        """
        Charge tous les produits et retourne un dict indexé par ID.
        
        Args:
            file_path: Chemin vers products.csv
            
        Returns:
            Dict[product_id, Product]
        """
        return self.repo.load_as_dict(file_path, 'id')
