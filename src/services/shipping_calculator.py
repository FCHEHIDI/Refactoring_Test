"""
Shipping Calculator
Centralise les calculs de frais de port dispersés dans le legacy.
"""

from ..models.shipping_zone import ShippingZone
from ..config.constants import (
    SHIPPING_FREE_THRESHOLD,
    WEIGHT_TIERS,
    REMOTE_ZONES,
    REMOTE_ZONE_MARKUP,
    HANDLING_FEE,
    HANDLING_TIERS
)


class ShippingCalculator:
    """
    Calculateur de frais de port.
    Responsabilité unique: calculer les frais de livraison.
    """
    
    def calculate(
        self,
        subtotal: float,
        weight: float,
        zone: ShippingZone | None,
        zone_name: str
    ) -> float:
        """
        Calcule les frais de port selon les règles complexes du legacy.
        
        Args:
            subtotal: Montant de la commande
            weight: Poids total en kg
            zone: Zone de livraison (objet ShippingZone)
            zone_name: Nom de la zone (pour vérifier si éloignée)
            
        Returns:
            Montant des frais de port
        """
        # Livraison gratuite si subtotal >= seuil
        if subtotal >= SHIPPING_FREE_THRESHOLD:
            # Mais frais de manutention si très lourd
            return self._calculate_heavy_handling(weight)
        
        # Sinon calcul standard
        return self._calculate_standard_shipping(weight, zone, zone_name)
    
    def _calculate_standard_shipping(
        self,
        weight: float,
        zone: ShippingZone | None,
        zone_name: str
    ) -> float:
        """Calcule les frais standard avec paliers de poids"""
        if not zone:
            # Fallback si zone inconnue (comportement legacy)
            zone = ShippingZone(zone='DEFAULT', base=5.0, per_kg=0.5)
        
        # Calcul par palier de poids
        if weight > WEIGHT_TIERS.HEAVY:
            ship = zone.base + (weight - WEIGHT_TIERS.HEAVY) * zone.per_kg
        elif weight > WEIGHT_TIERS.MEDIUM:
            # Palier intermédiaire (règle cachée legacy)
            ship = zone.base + (weight - WEIGHT_TIERS.MEDIUM) * 0.3
        else:
            ship = zone.base
        
        # Majoration zones éloignées
        if zone_name in REMOTE_ZONES:
            ship *= REMOTE_ZONE_MARKUP
        
        return ship
    
    def _calculate_heavy_handling(self, weight: float) -> float:
        """Frais de manutention pour livraison gratuite avec poids élevé"""
        if weight > WEIGHT_TIERS.VERY_HEAVY:
            return (weight - WEIGHT_TIERS.VERY_HEAVY) * 0.25
        return 0.0
    
    def calculate_handling_fee(self, item_count: int) -> float:
        """
        Calcule les frais de gestion selon le nombre d'articles.
        
        Args:
            item_count: Nombre d'articles dans la commande
            
        Returns:
            Frais de gestion
        """
        if item_count > HANDLING_TIERS.TIER_2:
            return HANDLING_FEE * 2  # Double pour grosses commandes
        if item_count > HANDLING_TIERS.TIER_1:
            return HANDLING_FEE
        return 0.0
