"""
Discount Calculator
Centralise tous les calculs de remises dispersés dans le legacy.
"""

from datetime import datetime
from ..config.constants import (
    DISCOUNT_TIERS,
    LOYALTY_TIERS,
    MAX_DISCOUNT,
    WEEKEND_BONUS_MULTIPLIER
)


class DiscountCalculator:
    """
    Calculateur de remises.
    Responsabilité unique: calculer les différents types de remises.
    """
    
    def calculate_volume_discount(
        self,
        subtotal: float,
        customer_level: str
    ) -> float:
        """
        Calcule la remise par volume selon les paliers.
        
        Note: Préserve le bug legacy où les paliers s'écrasent
        au lieu de cumuler (if sans elif).
        
        Args:
            subtotal: Montant total avant remise
            customer_level: Niveau du client (BASIC, PREMIUM, VIP)
            
        Returns:
            Montant de la remise
        """
        discount = 0.0
        
        # Bug legacy préservé: les if s'écrasent au lieu de cumuler
        if subtotal > DISCOUNT_TIERS.TIER_1:
            discount = subtotal * DISCOUNT_TIERS.RATE_1
        if subtotal > DISCOUNT_TIERS.TIER_2:
            discount = subtotal * DISCOUNT_TIERS.RATE_2
        if subtotal > DISCOUNT_TIERS.TIER_3:
            discount = subtotal * DISCOUNT_TIERS.RATE_3
        if subtotal > DISCOUNT_TIERS.TIER_4 and customer_level == 'PREMIUM':
            discount = subtotal * DISCOUNT_TIERS.RATE_4
        
        return discount
    
    def apply_weekend_bonus(
        self,
        discount: float,
        order_date: str
    ) -> float:
        """
        Applique un bonus de 5% sur la remise si commande passée le weekend.
        
        Args:
            discount: Montant de la remise de base
            order_date: Date de la commande (format YYYY-MM-DD)
            
        Returns:
            Remise avec bonus weekend appliqué si applicable
        """
        if not order_date:
            return discount
        
        try:
            dt = datetime.strptime(order_date, '%Y-%m-%d')
            # weekday: 0=Monday, 5=Saturday, 6=Sunday
            if dt.weekday() in (5, 6):
                return discount * WEEKEND_BONUS_MULTIPLIER
        except (ValueError, AttributeError):
            pass
        
        return discount
    
    def calculate_loyalty_discount(self, points: float) -> float:
        """
        Calcule la remise fidélité basée sur les points.
        
        Note: Même bug que volume_discount (écrasement des paliers).
        
        Args:
            points: Nombre de points de fidélité
            
        Returns:
            Montant de la remise fidélité
        """
        loyalty_discount = 0.0
        
        # Bug legacy préservé: écrasement au lieu de cumul
        if points > LOYALTY_TIERS.TIER_1:
            loyalty_discount = min(
                points * LOYALTY_TIERS.RATE_1,
                LOYALTY_TIERS.CAP_1
            )
        if points > LOYALTY_TIERS.TIER_2:
            loyalty_discount = min(
                points * LOYALTY_TIERS.RATE_2,
                LOYALTY_TIERS.CAP_2
            )
        
        return loyalty_discount
    
    def apply_max_discount_cap(
        self,
        volume_discount: float,
        loyalty_discount: float
    ) -> tuple[float, float]:
        """
        Applique le plafond global de remise.
        Si le total dépasse MAX_DISCOUNT, on ajuste proportionnellement.
        
        Args:
            volume_discount: Remise sur volume
            loyalty_discount: Remise fidélité
            
        Returns:
            Tuple (volume_discount_adjusted, loyalty_discount_adjusted)
        """
        total_discount = volume_discount + loyalty_discount
        
        if total_discount > MAX_DISCOUNT:
            # Ajustement proportionnel
            if total_discount > 0:
                ratio = MAX_DISCOUNT / total_discount
                return (
                    volume_discount * ratio,
                    loyalty_discount * ratio
                )
        
        return (volume_discount, loyalty_discount)
