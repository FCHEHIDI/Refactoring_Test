"""
Test Golden Master - Régression
Vérifie que le code refactoré produit exactement la même sortie que le legacy.
"""

import subprocess
import sys
from pathlib import Path


class TestGoldenMaster:
    """Test de non-régression basé sur comparaison de sortie"""
    
    @staticmethod
    def test_golden_master():
        """
        Test critique: compare la sortie du code refactoré avec la référence legacy.
        
        Ce test doit TOUJOURS passer pour garantir la non-régression.
        Si ce test échoue, le refactoring a changé le comportement observable.
        """
        base_path = Path(__file__).parent.parent
        
        # 1. Charger la sortie de référence (legacy)
        expected_path = base_path / 'legacy' / 'expected' / 'report.txt'
        
        if not expected_path.exists():
            raise FileNotFoundError(
                f"Référence golden master manquante: {expected_path}\n"
                f"Générer avec: python legacy/order_report_legacy.py > legacy/expected/report.txt"
            )
        
        with open(expected_path, 'r', encoding='utf-8') as f:
            expected_output = f.read()
        
        # 2. Exécuter le code refactoré
        refactored_script = base_path / 'src' / 'main.py'
        
        if not refactored_script.exists():
            raise FileNotFoundError(
                f"Code refactoré introuvable: {refactored_script}\n"
                f"Le refactoring n'a pas encore été fait."
            )
        
        result = subprocess.run(
            [sys.executable, str(refactored_script)],
            capture_output=True,
            text=True,
            cwd=str(base_path)
        )
        
        if result.returncode != 0:
            raise RuntimeError(
                f"Le code refactoré a planté:\n"
                f"STDERR: {result.stderr}\n"
                f"STDOUT: {result.stdout}"
            )
        
        actual_output = result.stdout
        
        # 3. Comparaison stricte caractère par caractère
        if expected_output != actual_output:
            # Afficher les différences pour debugging
            expected_lines = expected_output.splitlines()
            actual_lines = actual_output.splitlines()
            
            print("\n❌ GOLDEN MASTER FAILED - RÉGRESSION DÉTECTÉE ❌\n")
            print(f"Expected {len(expected_lines)} lines, got {len(actual_lines)} lines\n")
            
            # Trouver les différences
            max_lines = max(len(expected_lines), len(actual_lines))
            for i in range(max_lines):
                expected_line = expected_lines[i] if i < len(expected_lines) else '<MISSING>'
                actual_line = actual_lines[i] if i < len(actual_lines) else '<MISSING>'
                
                if expected_line != actual_line:
                    print(f"Line {i + 1} differs:")
                    print(f"  EXPECTED: {repr(expected_line)}")
                    print(f"  ACTUAL:   {repr(actual_line)}")
                    print()
            
            raise AssertionError(
                "Le code refactoré produit une sortie différente du legacy.\n"
                "Le comportement observable a changé - c'est une RÉGRESSION."
            )
        
        print("✅ GOLDEN MASTER PASSED - Aucune régression détectée")
        print(f"✅ Sortie identique: {len(expected_output)} caractères, "
              f"{len(expected_output.splitlines())} lignes")


def test_legacy_still_works():
    """
    Test de sécurité: vérifie que le legacy fonctionne toujours.
    Utile pour détecter si on a accidentellement modifié le legacy.
    """
    base_path = Path(__file__).parent.parent
    legacy_script = base_path / 'legacy' / 'order_report_legacy.py'
    
    result = subprocess.run(
        [sys.executable, str(legacy_script)],
        capture_output=True,
        text=True,
        cwd=str(base_path)
    )
    
    assert result.returncode == 0, (
        f"Le script legacy ne fonctionne plus!\n"
        f"STDERR: {result.stderr}"
    )
    
    assert len(result.stdout) > 0, "Le legacy ne produit aucune sortie"
    
    print("✅ Legacy script fonctionne correctement")


if __name__ == '__main__':
    """Permet de lancer les tests directement sans pytest"""
    print("=" * 70)
    print("TEST GOLDEN MASTER - Vérification de non-régression")
    print("=" * 70)
    print()
    
    try:
        print("Test 1: Vérification que le legacy fonctionne...")
        test_legacy_still_works()
        print()
        
        print("Test 2: Golden Master (comparaison legacy vs refactoré)...")
        TestGoldenMaster.test_golden_master()
        print()
        
        print("=" * 70)
        print("✅ TOUS LES TESTS PASSENT")
        print("=" * 70)
        
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ TEST ÉCHOUÉ")
        print("=" * 70)
        print(f"\nErreur: {e}")
        sys.exit(1)
