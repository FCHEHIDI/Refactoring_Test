"""
ShippingZone Model
Encapsule les données d'une zone de livraison.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ShippingZone:
    """
    Représente une zone de livraison avec ses tarifs.
    
    Attributes:
        zone: Nom de la zone (ex: ZONE1, ZONE2)
        base: Tarif de base pour cette zone
        per_kg: Tarif par kg supplémentaire
    """
    zone: str
    base: float
    per_kg: float = 0.5
    
    def __post_init__(self):
        """Validation des données"""
        if self.base < 0:
            raise ValueError(f"Le tarif de base ne peut pas être négatif: {self.base}")
        if self.per_kg < 0:
            raise ValueError(f"Le tarif par kg ne peut pas être négatif: {self.per_kg}")
