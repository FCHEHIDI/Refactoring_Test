"""
Order Processor
Orchestre les différents calculateurs pour traiter une commande client.
"""

from typing import List, Dict
from ..models.customer import Customer
from ..models.order import Order
from ..models.product import Product
from ..models.shipping_zone import ShippingZone
from ..models.order_summary import OrderSummary
from ..models.promotion import Promotion
from ..config.constants import MORNING_BONUS_RATE, MORNING_CUTOFF_HOUR, CURRENCY_RATES
from .discount_calculator import DiscountCalculator
from .tax_calculator import TaxCalculator
from .shipping_calculator import ShippingCalculator
from .loyalty_calculator import LoyaltyCalculator


class OrderProcessor:
    """
    Processeur de commandes.
    Responsabilité: orchestrer les calculateurs, pas faire les calculs.
    """
    
    def __init__(
        self,
        discount_calc: DiscountCalculator | None = None,
        tax_calc: TaxCalculator | None = None,
        shipping_calc: ShippingCalculator | None = None,
        loyalty_calc: LoyaltyCalculator | None = None
    ):
        """
        Args:
            discount_calc: Calculateur de remises (injection de dépendances)
            tax_calc: Calculateur de taxes
            shipping_calc: Calculateur de frais de port
            loyalty_calc: Calculateur de points fidélité
        """
        self.discount_calc = discount_calc or DiscountCalculator()
        self.tax_calc = tax_calc or TaxCalculator()
        self.shipping_calc = shipping_calc or ShippingCalculator()
        self.loyalty_calc = loyalty_calc or LoyaltyCalculator()
    
    def process_customer_orders(
        self,
        customer: Customer,
        orders: List[Order],
        products: Dict[str, Product],
        promotions: Dict[str, Promotion],
        shipping_zones: Dict[str, ShippingZone]
    ) -> OrderSummary:
        """
        Traite toutes les commandes d'un client et retourne le résumé.
        Fonction pure: pas de side effects.
        
        Args:
            customer: Le client
            orders: Ses commandes
            products: Dict des produits
            promotions: Dict des promotions
            shipping_zones: Dict des zones de livraison
            
        Returns:
            OrderSummary avec tous les montants calculés
        """
        # 1. Calculer subtotal et appliquer promotions
        subtotal, weight, morning_bonus = self._calculate_subtotal_with_promos(
            orders, products, promotions
        )
        
        # 2. Calculer points de fidélité
        loyalty_points = self.loyalty_calc.calculate_points(orders)
        
        # 3. Calculer remises
        volume_discount = self.discount_calc.calculate_volume_discount(
            subtotal, customer.level
        )
        
        # Appliquer bonus weekend sur remise volume
        first_order_date = orders[0].date if orders else ''
        volume_discount = self.discount_calc.apply_weekend_bonus(
            volume_discount, first_order_date
        )
        
        loyalty_discount = self.discount_calc.calculate_loyalty_discount(
            loyalty_points
        )
        
        # Appliquer plafond global
        volume_discount, loyalty_discount = \
            self.discount_calc.apply_max_discount_cap(
                volume_discount, loyalty_discount
            )
        
        # 4. Calculer taxe
        taxable_amount = subtotal - (volume_discount + loyalty_discount)
        tax = self.tax_calc.calculate(orders, products, taxable_amount)
        
        # 5. Calculer frais de port
        zone = shipping_zones.get(customer.shipping_zone)
        shipping = self.shipping_calc.calculate(
            subtotal, weight, zone, customer.shipping_zone
        )
        handling = self.shipping_calc.calculate_handling_fee(len(orders))
        
        # 6. Conversion devise
        currency_rate = CURRENCY_RATES.get(customer.currency, 1.0)
        
        # 7. Total final
        total = round(
            (taxable_amount + tax + shipping + handling) * currency_rate,
            2
        )
        
        return OrderSummary(
            customer=customer,
            subtotal=subtotal,
            volume_discount=volume_discount,
            loyalty_discount=loyalty_discount,
            tax=tax * currency_rate,
            shipping=shipping,
            handling=handling,
            total=total,
            loyalty_points=loyalty_points,
            weight=weight,
            morning_bonus=morning_bonus,
            item_count=len(orders)
        )
    
    def _calculate_subtotal_with_promos(
        self,
        orders: List[Order],
        products: Dict[str, Product],
        promotions: Dict[str, Promotion]
    ) -> tuple[float, float, float]:
        """
        Calcule le subtotal en appliquant les promotions et bonus matinaux.
        
        Returns:
            Tuple (subtotal, weight_total, morning_bonus_total)
        """
        subtotal = 0.0
        total_weight = 0.0
        total_morning_bonus = 0.0
        
        for order in orders:
            # Récupérer produit (avec fallback legacy)
            prod = products.get(order.product_id)
            if not prod:
                # Fallback: utiliser le prix de la commande
                base_price = order.unit_price
                weight = 1.0
            else:
                base_price = prod.price
                weight = prod.weight
            
            # Appliquer promo
            promo_code = order.promo_code
            discount_rate = 0.0
            fixed_discount = 0.0
            
            if promo_code and promo_code in promotions:
                promo = promotions[promo_code]
                if promo.active:
                    discount_rate = promo.get_discount_rate()
                    fixed_discount = promo.get_fixed_discount()
            
            # Calcul ligne avec promo
            # Bug legacy préservé: FIXED appliquée par ligne au lieu de global
            line_total = order.qty * base_price * (1 - discount_rate) - fixed_discount * order.qty
            
            # Bonus matinal (règle cachée: avant 10h)
            hour = order.get_hour()
            morning_bonus = 0.0
            if hour < MORNING_CUTOFF_HOUR:
                morning_bonus = line_total * MORNING_BONUS_RATE
                line_total = line_total - morning_bonus
            
            subtotal += line_total
            total_weight += weight * order.qty
            total_morning_bonus += morning_bonus
        
        return (subtotal, total_weight, total_morning_bonus)
