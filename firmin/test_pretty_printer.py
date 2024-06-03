import pytest
from lark import Tree, Token
from Parser import (
    pretty_print,
    pretty_printer_liste_var,
    pretty_printer_commande,
    pretty_printer_expression,
    parser
)

def test_pretty_printer():
    programme = """
    main(x, t1[10]) {
        x = 1 + 2;
        printf(x);
        return(x);
    }
    """
    arbre = parser.parse(programme)
    sortie_attendue = """main(x, t1[10]) {
 x = 1 + 2;
printf(x);
return(x);
}"""
    assert pretty_print(arbre) == sortie_attendue

def test_pretty_printer_liste_var():
    arbre = Tree('liste_normale', [Token('VARIABLE', 'x'), Token('TABLEAU', 't1[10]')])
    assert pretty_printer_liste_var(arbre) == "x, t1[10]"

def test_pretty_printer_commande():
    arbre_asgt = Tree('com_asgt', [Token('VARIABLE', 'x'), Tree('exp_binaire', [Token('NOMBRE', '1'), Token('OPBINAIRE', '+'), Token('NOMBRE', '2')])])
    assert pretty_printer_commande(arbre_asgt) == "x = 1 + 2;"

    arbre_printf = Tree('com_printf', [Token('VARIABLE', 'x')])
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

def test_pretty_printer_expression_access_table():
    arbre_access_table = Tree('access_table', [Token('ID_TABLEAU', 't1'), Tree('exp_nombre', [Token('NOMBRE', '10')])])
    assert pretty_printer_expression(arbre_access_table) == "t1[10]"

def test_pretty_printer_expression_binaire():
    arbre_exp_bin = Tree('exp_binaire', [Token('NOMBRE', '3'), Token('OPBINAIRE', '*'), Token('NOMBRE', '4')])
    assert pretty_printer_expression(arbre_exp_bin) == "3 * 4"

if __name__ == "__main__":
    pytest.main()
