"""
Loyalty Calculator
Calcule les points de fidélité.
"""

from typing import List
from ..models.order import Order
from ..config.constants import LOYALTY_POINTS_RATE


class LoyaltyCalculator:
    """
    Calculateur de points de fidélité.
    Responsabilité unique: calculer les points de fidélité.
    """
    
    def calculate_points(self, orders: List[Order]) -> float:
        """
        Calcule les points de fidélité basés sur le montant des commandes.
        
        Args:
            orders: Liste des commandes du client
            
        Returns:
            Nombre de points de fidélité (float)
        """
        total = sum(order.line_total() for order in orders)
        return total * LOYALTY_POINTS_RATE
