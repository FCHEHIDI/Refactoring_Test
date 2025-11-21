"""
Product Model
Encapsule les données et comportements liés à un produit.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    """
    Représente un produit du catalogue.
    
    Attributes:
        id: Identifiant unique du produit
        name: Nom du produit
        category: Catégorie du produit
        price: Prix unitaire
        weight: Poids en kg (défaut: 1.0)
        taxable: Si le produit est soumis à la taxe (défaut: True)
    """
    id: str
    name: str
    category: str
    price: float
    weight: float = 1.0
    taxable: bool = True
    
    def __post_init__(self):
        """Validation des données"""
        if self.price < 0:
            raise ValueError(f"Le prix ne peut pas être négatif: {self.price}")
        if self.weight < 0:
            raise ValueError(f"Le poids ne peut pas être négatif: {self.weight}")
