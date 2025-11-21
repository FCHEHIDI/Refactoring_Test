"""
Customer Model
Encapsule les données et comportements liés à un client.
"""

from dataclasses import dataclass
from typing import Literal


CustomerLevel = Literal['BASIC', 'PREMIUM', 'VIP']
Currency = Literal['EUR', 'USD', 'GBP']


@dataclass(frozen=True)
class Customer:
    """
    Représente un client du système.
    
    Attributes:
        id: Identifiant unique du client
        name: Nom complet du client
        level: Niveau de fidélité (BASIC, PREMIUM, VIP)
        shipping_zone: Zone de livraison (ZONE1, ZONE2, etc.)
        currency: Devise préférée du client
    """
    id: str
    name: str
    level: CustomerLevel = 'BASIC'
    shipping_zone: str = 'ZONE1'
    currency: Currency = 'EUR'
    
    def is_premium(self) -> bool:
        """Vérifie si le client a le statut premium ou supérieur"""
        return self.level in ('PREMIUM', 'VIP')
    
    def is_vip(self) -> bool:
        """Vérifie si le client a le statut VIP"""
        return self.level == 'VIP'
