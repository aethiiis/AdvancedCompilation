import lark

grammaire = """
%import common.SIGNED_NUMBER  #bibliothèque lark.
%import common.WS
%ignore WS
// %ignore /[ ]/   #ignore les blancs, mais l'arbre ne contient pas l'information de leur existence. problématique du pretty printer. 

VARIABLE : /[a-su-zA-SU-Z_][a-zA-Z0-9]*/
NOMBRE : SIGNED_NUMBER
ID_TABLEAU : /[t][a-zA-Z 0-9]*/  
// NOMBRE : /[1-9][0-9]*/
OPBINAIRE: /[+*\/&><]/|">="|"-"|">>"  //lark essaie de faire les tokens les plus long possible
TABLEAU : ID_TABLEAU"["NOMBRE"]" | "["NOMBRE ("," NOMBRE)*"]" | "[" "]"

expression: VARIABLE -> exp_variable
| NOMBRE         -> exp_nombre
| ID_TABLEAU"["expression"]"       -> access_table
| "len" "(" ID_TABLEAU ")"       -> exp_len_tableau
| expression OPBINAIRE expression -> exp_binaire

commande : VARIABLE "=" expression ";"-> com_asgt //les exp entre "" ne sont pas reconnues dans l'arbre syntaxique
| "printf" "(" expression ")" ";" -> com_printf
| commande+ -> com_sequence
| "while" "(" expression ")" "{" commande "}" -> com_while
| "if" "(" expression ")" "{" commande "}" "else" "{" commande "}" -> com_if
| "var" TABLEAU ("=" TABLEAU)? ";"  -> com_decla_tableau
| ID_TABLEAU"["NOMBRE"]" "=" expression ";" -> com_assgt_tableau

liste_elmts :                -> liste_vide
| (VARIABLE|TABLEAU) ("," (VARIABLE|TABLEAU))* -> liste_normale

list_expression : -> list_vide_expression
| expression(","expression)* -> liste_normale_expression

programme : "main" "(" liste_elmts ")" "{" commande "return" "(" list_expression ")" ";" "}" -> prog_main // ressemble à une déclaration de fonction
"""
parser = lark.Lark(grammaire, start="programme")



def pretty_printer_programme(tree):
    return "main(%s) {\n %s \nreturn(%s);\n}" % (
        pretty_printer_liste_elmts(tree.children[0]),
        pretty_printer_commande(tree.children[1]),
        pretty_printer_list_expression(tree.children[2])
    )

def pretty_printer_list_expression(tree):
    if tree.data == "liste_vide_expression":
        return ""
    else:
        char = ""
        for child in tree.children :
         
            char += f"{child.children[0]},"
        char = char[:-1]
    return char

def pretty_printer_liste_elmts(tree):
    if tree.data == "liste_vide":
        return ""
    else:
        return ", ".join([t.value for t in tree.children])

def pretty_printer_commande(tree):
    if tree.data == "com_asgt":
        return f"{tree.children[0].value} = {pretty_printer_expression(tree.children[1])};"
    elif tree.data == "com_print":
        return f"printf({pretty_printer_expression(tree.children[0])});"
    elif tree.data == "com_sequence":
        return "\n".join([pretty_printer_commande(c) for c in tree.children])
    elif tree.data == "com_while":
        return f"while({pretty_printer_expression(tree.children[0])}) {{\n{pretty_printer_commande(tree.children[1])}\n}}"
    elif tree.data == "com_if":
        return f"if({pretty_printer_expression(tree.children[0])}) {{\n{pretty_printer_commande(tree.children[1])}\n}} else {{\n{pretty_printer_commande(tree.children[2])}\n}}"
    elif tree.data == "com_decla_tableau":

        try :
            return f"var {tree.children[0].value} = {tree.children[1].value};"
        except Exception as e: 
            return f"var {tree.children[0].value};"

    elif tree.data == "com_assgt_tableau":
        return f"{tree.children[0].value}[{tree.children[1].value}] = {pretty_printer_expression(tree.children[2])};"


def pretty_printer_expression(tree):
    if isinstance(tree, lark.Token):
        return str(tree)
    elif tree.data == "exp_variable":
        return tree.children[0].value
    elif tree.data == "exp_nombre":
        return tree.children[0].value
    elif tree.data == "access_table":
        return f"{tree.children[0].value}[{pretty_printer_expression(tree.children[1])}]"
    elif tree.data == "exp_len_tableau" :
        return f"len({pretty_printer_expression(tree.children[0])})"
    elif tree.data == "exp_binaire":
        return f"{pretty_printer_expression(tree.children[0])} {tree.children[1].value} {pretty_printer_expression(tree.children[2])}"

def pretty_print(tree):
    print(pretty_printer_programme(tree))
