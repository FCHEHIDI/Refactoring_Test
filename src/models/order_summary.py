"""
OrderSummary Model
Encapsule le résultat des calculs pour un client.
"""

from dataclasses import dataclass
from .customer import Customer


@dataclass(frozen=True)
class OrderSummary:
    """
    Représente le résumé calculé d'une commande client.
    Contient tous les montants calculés pour la génération du rapport.
    
    Attributes:
        customer: Le client concerné
        subtotal: Sous-total avant remises
        volume_discount: Remise sur volume
        loyalty_discount: Remise fidélité
        morning_bonus: Bonus matinal (si applicable)
        tax: Montant de la taxe
        shipping: Frais de port
        handling: Frais de gestion
        total: Total final
        loyalty_points: Points de fidélité du client
        weight: Poids total de la commande
        item_count: Nombre d'articles
    """
    customer: Customer
    subtotal: float
    volume_discount: float
    loyalty_discount: float
    tax: float
    shipping: float
    handling: float
    total: float
    loyalty_points: float
    weight: float
    morning_bonus: float = 0.0
    item_count: int = 0
    
    @property
    def total_discount(self) -> float:
        """Calcule le total des remises"""
        return self.volume_discount + self.loyalty_discount
    
    @property
    def taxable_amount(self) -> float:
        """Calcule le montant taxable"""
        return self.subtotal - self.total_discount
