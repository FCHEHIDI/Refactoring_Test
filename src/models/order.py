"""
Order Model
Encapsule les données d'une commande.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Order:
    """
    Représente une ligne de commande.
    
    Attributes:
        id: Identifiant unique de la commande
        customer_id: Identifiant du client
        product_id: Identifiant du produit
        qty: Quantité commandée
        unit_price: Prix unitaire au moment de la commande
        date: Date de la commande (format YYYY-MM-DD)
        promo_code: Code promo appliqué (optionnel)
        time: Heure de la commande (format HH:MM)
    """
    id: str
    customer_id: str
    product_id: str
    qty: int
    unit_price: float
    date: str = ''
    promo_code: str = ''
    time: str = '12:00'
    
    def __post_init__(self):
        """Validation des données"""
        if self.qty <= 0:
            raise ValueError(f"La quantité doit être positive: {self.qty}")
        if self.unit_price < 0:
            raise ValueError(f"Le prix unitaire ne peut pas être négatif: {self.unit_price}")
    
    def get_hour(self) -> int:
        """Extrait l'heure de la commande"""
        try:
            return int(self.time.split(':')[0])
        except (ValueError, IndexError):
            return 12  # Heure par défaut
    
    def line_total(self) -> float:
        """Calcule le total de la ligne (quantité × prix)"""
        return self.qty * self.unit_price
