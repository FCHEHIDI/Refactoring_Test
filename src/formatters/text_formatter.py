"""
Text Report Formatter
Génère le rapport texte dans le format legacy.
"""

import math
from typing import List
from ..models.order_summary import OrderSummary


class TextReportFormatter:
    """
    Formateur de rapport texte.
    Responsabilité: transformer des OrderSummary en texte formaté.
    Fonction pure: pas de side effects.
    """
    
    def format(self, summaries: List[OrderSummary]) -> str:
        """
        Génère le rapport texte complet pour tous les clients.
        
        Args:
            summaries: Liste des résumés de commandes
            
        Returns:
            Rapport texte formaté (compatible legacy)
        """
        lines = []
        grand_total = 0.0
        total_tax_collected = 0.0
        
        for summary in summaries:
            lines.extend(self._format_customer(summary))
            lines.append('')  # Ligne vide entre clients
            
            grand_total += summary.total
            total_tax_collected += summary.tax
        
        # Totaux globaux
        lines.append(f'Grand Total: {grand_total:.2f} EUR')
        lines.append(f'Total Tax Collected: {total_tax_collected:.2f} EUR')
        
        return '\n'.join(lines)
    
    def _format_customer(self, summary: OrderSummary) -> List[str]:
        """
        Formate la section d'un client.
        
        Args:
            summary: Résumé de commande du client
            
        Returns:
            Liste de lignes formatées
        """
        c = summary.customer
        lines = []
        
        # En-tête client
        lines.append(f'Customer: {c.name} ({c.id})')
        lines.append(f'Level: {c.level} | Zone: {c.shipping_zone} | Currency: {c.currency}')
        
        # Montants
        lines.append(f'Subtotal: {summary.subtotal:.2f}')
        lines.append(f'Discount: {summary.total_discount:.2f}')
        lines.append(f'  - Volume discount: {summary.volume_discount:.2f}')
        lines.append(f'  - Loyalty discount: {summary.loyalty_discount:.2f}')
        
        # Bonus matinal (uniquement si > 0)
        if summary.morning_bonus > 0:
            lines.append(f'  - Morning bonus: {summary.morning_bonus:.2f}')
        
        # Taxe et frais
        lines.append(f'Tax: {summary.tax:.2f}')
        lines.append(f'Shipping ({c.shipping_zone}, {summary.weight:.1f}kg): {summary.shipping:.2f}')
        
        # Frais de gestion (uniquement si > 0)
        if summary.handling > 0:
            lines.append(f'Handling ({summary.item_count} items): {summary.handling:.2f}')
        
        # Total et points
        lines.append(f'Total: {summary.total:.2f} {c.currency}')
        lines.append(f'Loyalty Points: {math.floor(summary.loyalty_points)}')
        
        return lines
