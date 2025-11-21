"""
Constants - Centralisation de toutes les constantes métier
Résout le problème des "magic numbers" dispersés dans le legacy.
"""

from dataclasses import dataclass


# === TAXES ===
TAX_RATE = 0.2  # 20%


# === SHIPPING ===
SHIPPING_FREE_THRESHOLD = 50.0  # Livraison gratuite au-dessus de ce montant
HANDLING_FEE = 2.5  # Frais de gestion par défaut
REMOTE_ZONE_MARKUP = 1.2  # Majoration 20% pour zones éloignées
REMOTE_ZONES = {'ZONE3', 'ZONE4'}  # Zones considérées comme éloignées


# === DISCOUNTS ===
MAX_DISCOUNT = 200.0  # Plafond global de remise


# === LOYALTY ===
LOYALTY_POINTS_RATE = 0.01  # 1% du montant en points


# === BONUSES ===
MORNING_BONUS_RATE = 0.03  # 3% de bonus avant 10h
MORNING_CUTOFF_HOUR = 10  # Heure limite pour bonus matinal
WEEKEND_BONUS_MULTIPLIER = 1.05  # 5% de bonus sur remise le weekend


# === CURRENCY ===
CURRENCY_RATES = {
    'EUR': 1.0,
    'USD': 1.1,
    'GBP': 0.85
}


@dataclass(frozen=True)
class DiscountTiers:
    """
    Paliers de remise par volume.
    
    Note: Le legacy a un bug où les paliers s'écrasent au lieu de cumuler.
    On préserve ce comportement pour la non-régression.
    """
    # Palier 1: > 50€
    TIER_1: float = 50.0
    RATE_1: float = 0.05  # 5%
    
    # Palier 2: > 100€
    TIER_2: float = 100.0
    RATE_2: float = 0.10  # 10%
    
    # Palier 3: > 500€
    TIER_3: float = 500.0
    RATE_3: float = 0.15  # 15%
    
    # Palier 4: > 1000€ (PREMIUM uniquement)
    TIER_4: float = 1000.0
    RATE_4: float = 0.20  # 20%


@dataclass(frozen=True)
class LoyaltyTiers:
    """
    Paliers de remise fidélité basés sur les points.
    
    Note: Même bug que les remises volume (écrasement au lieu de cumul).
    """
    # Palier 1: > 100 points
    TIER_1: float = 100.0
    RATE_1: float = 0.1  # 10% des points
    CAP_1: float = 50.0  # Plafonné à 50€
    
    # Palier 2: > 500 points
    TIER_2: float = 500.0
    RATE_2: float = 0.15  # 15% des points
    CAP_2: float = 100.0  # Plafonné à 100€


@dataclass(frozen=True)
class WeightTiers:
    """Paliers de poids pour calcul des frais de port"""
    MEDIUM: float = 5.0  # Palier poids moyen
    HEAVY: float = 10.0  # Palier poids lourd
    VERY_HEAVY: float = 20.0  # Palier très lourd (frais de manutention)


@dataclass(frozen=True)
class HandlingTiers:
    """Paliers de nombre d'articles pour frais de gestion"""
    TIER_1: int = 10  # > 10 articles
    TIER_2: int = 20  # > 20 articles (double)


# Instances par défaut (singleton pattern)
DISCOUNT_TIERS = DiscountTiers()
LOYALTY_TIERS = LoyaltyTiers()
WEIGHT_TIERS = WeightTiers()
HANDLING_TIERS = HandlingTiers()
