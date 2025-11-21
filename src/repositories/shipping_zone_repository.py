"""
ShippingZone Repository
Gère le chargement des zones de livraison depuis CSV.
"""

from pathlib import Path
from typing import Dict
from .csv_repository import CSVRepository
from ..models.shipping_zone import ShippingZone


class ShippingZoneRepository:
    """Repository pour charger les zones de livraison depuis shipping_zones.csv"""
    
    def __init__(self):
        self.repo = CSVRepository(self._map_shipping_zone)
    
    def _map_shipping_zone(self, row: dict) -> ShippingZone:
        """
        Transforme une ligne CSV en objet ShippingZone.
        
        Préserve le comportement legacy:
        - per_kg avec valeur par défaut 0.5
        """
        return ShippingZone(
            zone=row['zone'],
            base=float(row['base']),
            per_kg=float(row.get('per_kg', '0.5'))
        )
    
    def load_all(self, file_path: Path | str) -> Dict[str, ShippingZone]:
        """
        Charge toutes les zones et retourne un dict indexé par nom de zone.
        
        Args:
            file_path: Chemin vers shipping_zones.csv
            
        Returns:
            Dict[zone_name, ShippingZone]
        """
        return self.repo.load_as_dict(file_path, 'zone')
