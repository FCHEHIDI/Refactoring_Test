"""
Promotion Repository
Gère le chargement des promotions depuis CSV.
"""

from pathlib import Path
from typing import Dict
from .csv_repository import CSVRepository
from ..models.promotion import Promotion


class PromotionRepository:
    """Repository pour charger les promotions depuis promotions.csv"""
    
    def __init__(self):
        self.repo = CSVRepository(self._map_promotion)
    
    def _map_promotion(self, row: dict) -> Promotion:
        """
        Transforme une ligne CSV en objet Promotion.
        
        Préserve le comportement legacy:
        - Active par défaut
        - Valeur par défaut si colonne manquante
        """
        return Promotion(
            code=row['code'],
            type=row['type'],
            value=float(row['value']),
            active=row.get('active', 'true').lower() != 'false'
        )
    
    def load_all(self, file_path: Path | str) -> Dict[str, Promotion]:
        """
        Charge toutes les promotions et retourne un dict indexé par code.
        
        Args:
            file_path: Chemin vers promotions.csv
            
        Returns:
            Dict[promo_code, Promotion]
            
        Note:
            Le legacy ignore silencieusement si le fichier n'existe pas.
            On préserve ce comportement.
        """
        try:
            return self.repo.load_as_dict(file_path, 'code')
        except FileNotFoundError:
            # Comportement legacy: retourne dict vide si fichier manquant
            return {}
