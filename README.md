# Order Report Refactoring

Refactoring d'un système legacy de génération de rapports de commandes.

## 🎯 Objectif

Refactorer le code legacy (`legacy/order_report_legacy.py`) tout en garantissant la non-régression fonctionnelle via un test golden master.

## 📦 Installation

### Prérequis
- Python 3.10+
- pip

### Installation des dépendances

```bash
# Dépendances de production
pip install -r requirements.txt

# Dépendances de développement (inclut pytest)
pip install -r requirements-dev.txt
```

## 🧪 Tests

### Générer la référence golden master

Si ce n'est pas déjà fait, générer la sortie de référence du legacy :

```bash
python legacy/order_report_legacy.py > legacy/expected/report.txt
```

### Lancer les tests

```bash
# Avec pytest (recommandé)
pytest

# Ou directement le test golden master
python tests/test_golden_master.py
```

### Test Golden Master

Le test golden master vérifie que le code refactoré produit **exactement** la même sortie que le code legacy, caractère par caractère.

**Status actuel** : ❌ Le code refactoré n'existe pas encore (`src/main.py`)

## 📁 Structure du Projet

```
Refactoring_Test/
├── legacy/                      # ❌ NE PAS MODIFIER
│   ├── order_report_legacy.py   # Script original
│   ├── data/                    # Données CSV
│   └── expected/                # Sortie de référence
│       └── report.txt
│
├── src/                         # 🔨 Code refactoré (à créer)
│   └── main.py                  # Point d'entrée
│
├── tests/                       # 🧪 Tests
│   └── test_golden_master.py    # Test de non-régression
│
├── requirements.txt             # Dépendances production
├── requirements-dev.txt         # Dépendances développement
└── README.md                    # Ce fichier
```

## 📊 Analyse du Legacy

Voir [ANALYSE_LEGACY.md](./ANALYSE_LEGACY.md) pour l'analyse détaillée des problèmes et l'architecture proposée.

### Problèmes Principaux Identifiés

1. **God Function** : 280+ lignes dans une seule fonction
2. **Pas d'encapsulation** : Tout en dictionnaires anonymes
3. **Duplication** : 4 méthodes différentes pour parser des CSV
4. **Logique dispersée** : Calculs métier éparpillés partout
5. **Magic numbers** : Constantes hardcodées
6. **Pas de types** : Code non typé

## 🏗️ Plan de Refactoring

### Phase 1: Setup ✅
- [x] Analyse du legacy
- [x] Test golden master
- [x] Structure projet

### Phase 2: Models (à faire)
- [ ] Créer dataclasses typées
- [ ] Customer, Product, Order, etc.

### Phase 3: Repositories (à faire)
- [ ] CSVRepository générique
- [ ] Repositories spécifiques

### Phase 4: Services (à faire)
- [ ] DiscountCalculator
- [ ] TaxCalculator
- [ ] ShippingCalculator
- [ ] OrderProcessor

### Phase 5: Formatters (à faire)
- [ ] TextReportFormatter

### Phase 6: Main (à faire)
- [ ] Point d'entrée orchestration

## 👤 Auteur

**Fares Chehidi**
- GitHub: [@FCHEHIDI](https://github.com/FCHEHIDI)
- Email: fareschehidi7@gmail.com

## 📝 Licence

Projet d'exercice - Refactoring de code legacy
