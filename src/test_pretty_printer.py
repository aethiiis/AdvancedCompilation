import lark
import pytest
from lark import Tree, Token

# Importer les fonctions que vous voulez tester
from Parser import (
    pretty_printer_programme,
    pretty_printer_liste_elmts,
    pretty_printer_commande,
    pretty_printer_expression,
    parser
)

# Exemple de programme pour le test
exemple_programme = """
main() {
    var t1[10];
    x = 1 + 2;
    printf(x);
    return(x);
}
"""

# Arbre syntaxique attendu pour l'exemple de programme
attendu_arbre = parser.parse(exemple_programme)

def test_pretty_printer_programme():
    sortie_attendue = """main() {
 var t1[10];
x = 1 + 2;
printf(x);
return(x);
}"""
    assert pretty_printer_programme(attendu_arbre) == sortie_attendue

def test_pretty_printer_liste_elmts():
    arbre = Tree('liste_normale', [Token('VARIABLE', 'x'), Token('TABLEAU', 't1[10]')])
    assert pretty_printer_liste_elmts(arbre) == "x, t1[10]"

def test_pretty_printer_commande():
    arbre_asgt = Tree('com_asgt', [Token('VARIABLE', 'x'), Tree('exp_binaire', [Token('NOMBRE', '1'), Token('OPBINAIRE', '+'), Token('NOMBRE', '2')])])
    assert pretty_printer_commande(arbre_asgt) == "x = 1 + 2;"

    arbre_printf = Tree('com_print', [Token('VARIABLE', 'x')])
    assert pretty_printer_commande(arbre_printf) == "printf(x);"

def test_pretty_printer_expression():
    arbre_exp = Tree('exp_binaire', [Token('NOMBRE', '1'), Token('OPBINAIRE', '+'), Token('NOMBRE', '2')])
    assert pretty_printer_expression(arbre_exp) == "1 + 2"

def test_pretty_printer_expression_variable():
    arbre_exp_var = Tree('exp_variable', [Token('VARIABLE', 'x')])
    assert pretty_printer_expression(arbre_exp_var) == "x"

def test_pretty_printer_expression_nombre():
    arbre_exp_num = Tree('exp_nombre', [Token('NOMBRE', '1')])
    assert pretty_printer_expression(arbre_exp_num) == "1"

if __name__ == "__main__":
    pytest.main()
