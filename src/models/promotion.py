"""
Promotion Model
Encapsule les données d'une promotion.
"""

from dataclasses import dataclass
from typing import Literal


PromotionType = Literal['PERCENTAGE', 'FIXED']


@dataclass(frozen=True)
class Promotion:
    """
    Représente une promotion commerciale.
    
    Attributes:
        code: Code promo unique
        type: Type de promotion (PERCENTAGE ou FIXED)
        value: Valeur de la promotion (pourcentage ou montant fixe)
        active: Si la promotion est active (défaut: True)
    """
    code: str
    type: PromotionType
    value: float
    active: bool = True
    
    def get_discount_rate(self) -> float:
        """Retourne le taux de réduction si c'est un pourcentage, sinon 0"""
        if self.type == 'PERCENTAGE':
            return self.value / 100.0
        return 0.0
    
    def get_fixed_discount(self) -> float:
        """Retourne le montant fixe si c'est une remise fixe, sinon 0"""
        if self.type == 'FIXED':
            return self.value
        return 0.0
