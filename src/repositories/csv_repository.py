"""
Generic CSV Repository
Résout le problème des 4 méthodes différentes de parsing dans le legacy.
"""

import csv
from pathlib import Path
from typing import TypeVar, Generic, Callable, List, Dict


T = TypeVar('T')


class CSVRepository(Generic[T]):
    """
    Repository générique pour charger des fichiers CSV.
    
    Unifie les 4 méthodes différentes du legacy:
    - csv.reader + itération manuelle
    - readlines() + split(',')
    - csv.DictReader
    - read() + split('\n')
    
    Utilise maintenant une seule méthode: csv.DictReader
    
    Attributes:
        mapper: Fonction qui transforme un dict (ligne CSV) en objet typé
    """
    
    def __init__(self, mapper: Callable[[Dict[str, str]], T]):
        """
        Args:
            mapper: Fonction qui prend un dict et retourne une instance de T
        """
        self.mapper = mapper
    
    def load(self, file_path: Path | str) -> List[T]:
        """
        Charge un fichier CSV et le transforme en liste d'objets typés.
        
        Args:
            file_path: Chemin vers le fichier CSV
            
        Returns:
            Liste d'objets typés
            
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            ValueError: Si le parsing échoue
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Fichier CSV introuvable: {file_path}")
        
        results = []
        errors = []
        
        with open(file_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            
            for line_num, row in enumerate(reader, start=2):  # start=2 car ligne 1 = header
                try:
                    obj = self.mapper(row)
                    results.append(obj)
                except Exception as e:
                    # Contrairement au legacy qui ignore silencieusement,
                    # on collecte les erreurs pour debugging
                    errors.append(f"Line {line_num}: {e}")
        
        # Pour compatibilité legacy, on n'échoue pas si des lignes sont invalides
        # mais on pourrait logger les erreurs en production
        if errors and len(results) == 0:
            # Si AUCUNE ligne n'est valide, c'est probablement un vrai problème
            raise ValueError(f"Impossible de parser {file_path}:\n" + "\n".join(errors[:5]))
        
        return results
    
    def load_as_dict(self, file_path: Path | str, key_attr: str) -> Dict[str, T]:
        """
        Charge un fichier CSV et retourne un dictionnaire indexé par une clé.
        
        Args:
            file_path: Chemin vers le fichier CSV
            key_attr: Nom de l'attribut à utiliser comme clé
            
        Returns:
            Dictionnaire {clé: objet}
        """
        items = self.load(file_path)
        return {getattr(item, key_attr): item for item in items}
