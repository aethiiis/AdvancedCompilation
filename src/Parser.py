import lark

grammaire = """
%import common.SIGNED_NUMBER  #bibliothèque lark.
%import common.WS
%ignore WS
// %ignore /[ ]/   #ignore les blancs, mais l'arbre ne contient pas l'information de leur existence. problématique du pretty printer. 

VARIABLE : /[a-zA-Z_][a-zA-Z0-9]*/
NOMBRE : SIGNED_NUMBER
// NOMBRE : /[1-9][0-9]*/
OPBINAIRE: /[+*\/&><]/|">="|"-"|">>"  //lark essaie de faire les tokens les plus long possible
FONCTION_NAME : /[a-su-zA-SU-Z_][a-zA-Z0-9]*/
ID_TABLEAU : /[t][a-zA-Z 0-9]*/ 
TABLEAU : ID_TABLEAU"["NOMBRE"]"

expression: VARIABLE -> exp_variable
| TABLEAU -> exp_tableau
| NOMBRE         -> exp_nombre
| expression OPBINAIRE expression -> exp_binaire
| ID_TABLEAU"["expression"]"       -> access_table
| "len" "(" ID_TABLEAU ")"       -> exp_len_tableau


commande : -> com_vide
| VARIABLE "=" expression ";"-> com_asgt //les exp entre "" ne sont pas reconnues dans l'arbre syntaxique
| "printf" "(" expression ")" ";" -> com_printf
| commande+ -> com_sequence
| "while" "(" expression ")" "{" commande "}" -> com_while
| "if" "(" expression ")" "{" commande "}" "else" "{" commande "}" -> com_if
| VARIABLE "=" FONCTION_NAME "(" liste_var ");" -> com_appel
| "var" TABLEAU ";"  -> com_decla_tableau
| ID_TABLEAU"["NOMBRE"]" "=" expression ";" -> com_assgt_tableau

fonction : FONCTION_NAME "(" liste_var ")" "{" commande "return" "(" expression ")" ";" "}" -> fonction

fonction_main : "main" "(" liste_var ")" "{" commande "return" "(" expression ")" ";" "}" -> fonction_main

liste_var :                -> liste_vide
| (expression) ("," (expression))* -> liste_normale

liste_fonction :           -> liste_fonction_vide
| fonction* -> liste_fonction

programme : liste_fonction fonction_main -> prog // ressemble à une déclaration de fonction
"""

parser = lark.Lark(grammaire, start = "programme")

def pretty_printer_liste_var(tree):
    if tree.data == "liste_vide":
        return ""
    else:
        return ", ".join([t.children[0].value for t in tree.children])    

def pretty_printer_expression(t):
    if isinstance(t, lark.Token):
        return str(t)
    elif t.data == "exp_variable":
        return t.children[0].value
    elif t.data == "exp_nombre":
        return t.children[0].value
    elif t.data == "access_table":
        return f"{t.children[0].value}[{pretty_printer_expression(t.children[1])}]"
    elif t.data == "exp_binaire":
        return f"{pretty_printer_expression(t.children[0])} {t.children[1].value} {pretty_printer_expression(t.children[2])}"

def pretty_printer_commande(t):
    if t.data == "com_vide":
        return ""
    if t.data == "com_asgt":
        return f"{t.children[0].value} = {pretty_printer_expression(t.children[1])} ;"
    if t.data == "com_printf":
        return f"printf ({pretty_printer_expression(t.children[0])}) ;"
    if t.data == "com_while":
        return "while (%s) {\n%s\n}\n" % (pretty_printer_expression(t.children[0]), pretty_printer_commande(t.children[1]))
    if t.data == "com_if":
        return "if (%s){ %s} else { %s}" % (pretty_printer_expression(t.children[0]), pretty_printer_commande(t.children[1]), pretty_printer_commande(t.children[2]))
    if t.data == "com_sequence":
        return "\n".join([pretty_printer_commande(u) for u in t.children])
    if t.data == "com_appel":
        return f"{t.children[0].value} = {t.children[1].value} ({pretty_printer_liste_var(t.children[2])}) ;"
    elif t.data == "com_decla_tableau":
        return f"var {t.children[0].value};"
    elif t.data == "com_assgt_tableau":
        return f"{t.children[0].value}[{t.children[1].value}] = {pretty_printer_expression(t.children[2])};"
    
def pretty_printer_fonction(t):
    return  "%s (%s) {\n%s\nreturn (%s);\n}" % (t.children[0].value, pretty_printer_expression(t.children[1]), pretty_printer_commande(t.children[2]), pretty_printer_expression(t.children[3]))

def pretty_printer_main(t):
    return "main (%s) {\n%sreturn (%s);\n}" % (pretty_printer_liste_var(t.children[0]), 
                                                pretty_printer_commande(t.children[1]),
                                                pretty_printer_expression(t.children[2]))

def pretty_print(t):
    if t.data == "liste_fonction_vide":
        return pretty_printer_main(t.children[0])
    return  "\n".join([pretty_printer_fonction(u) for u in t.children[0].children]) + "\n" + pretty_printer_main(t.children[1])


if __name__ == "__main__":
    t = parser.parse("""
                fonction1(x,y){
                    var t1[4];
                    t1[0] = 1;
                    return (x+y);
                }
                fonction2(x,y){
                    return (x*y);
                }
                main(x,y){
                while(x) {
                   y = y + 1;
                   z = fonction1(x,y);
                   printf(z);
                }
                return (y);
                }
                 """)
    print(t)
    print("#################")
    print(pretty_print(t))
