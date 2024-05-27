import lark


grammaire = """
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS

//
OPBINAIRE : /[+\*\/&|<>]/|"<="|">="|"=="|"-"|"!="|"<<"|">>"
VARIABLE : /[a-zA-Z_][a-zA-Z_0-9]*/
NOMBRE : SIGNED_NUMBER

//
expression : VARIABLE                                                                   -> exp_variable 
| NOMBRE                                                                                -> exp_nombre
| expression OPBINAIRE expression                                                       -> exp_binaire

commande : VARIABLE "=" expression ";"                                                  -> com_asgt
| "printf" "(" expression ")" ";"                                                       -> com_print
| commande+                                                                             -> com_sequence
| "while" "(" expression ")" "{" commande "}"                                           -> com_while
| "if" "(" expression ")" "{" commande "}" "else" "{" commande "}"                      -> com_if

liste_var :                                                                             -> liste_vide
| VARIABLE ("," VARIABLE)*                                                              -> liste_normale

programme : "main" "(" liste_var ")" "{" commande "return" "(" expression ")" ";" "}"   -> prog_main
"""

# def pretty_printer_programme(tree):
#     return "main(%s) {\n %s return(%s);\n}" % (pretty_printer_liste_var(tree.children[0]), pretty_printer_commande(tree.children[1]), pretty_printer_expression(tree.children[2]))

# def pretty_printer_liste_var(tree):
#     if t.data == "liste_vide":
#         return ""
#     else:
#         return ", ".join([t.value for t in tree.children])
    
# def pretty_printer_commande(tree):
#     if t.data == "com_asgt":
#         f"{t.children[0].value} = {pretty_printer_expression(t.children[1])};"
#     elif t.data == "com_print":
#         return f"printf({pretty_printer_expression(t.children[0])});"
#     elif t.data == "com_sequence":
#         return "\n".join([pretty_printer_commande(c) for c in t.children])
#     elif t.data == "com_while":
#         return "while(%s) {\n%s}"(pretty_printer_expression(t.children[0]), pretty_printer_commande(t.children[1]))
#     elif t.data == "com_if":
#         return "if(" + pretty_printer_expression(t.children[0]) + ") {\n" + pretty_printer_commande(t.children[1]) + "} else {\n" + pretty_printer_commande(t.children[2]) + "}"

# def pretty_printer_expression(tree):
#     if isinstance(tree, lark.Token):
#         return str(tree)
#     elif t.data == "exp_variable":
#         return t.children[0].value
#     elif t.data == "exp_nombre":
#         return t.children[0].value
#     return f"{pretty_printer_expression(t.children[0])} {t.children[1].value} {pretty_printer_expression(t.children[2])}"

parser = lark.Lark(grammaire, start="programme")

t = parser.parse("""main(x, x2) {
                        while(x) {
                            printf(x2 >> 13);
                            x = x + 1;
                        }
                        return(x);
                    }""")
print(t.pretty())

variables = t.children[0]
print(t.children[0].pretty())
programme = t.children[1]
print(t.children[1].pretty())



def compilExpression(ast):
    if ast.data == "exp_variable":
        return f"mov rax, [{ast.children[0].value}]\n"
    elif ast.data == "exp_nombre":
        return f"mov rax, {ast.children[0].value}\n"
    elif ast.data == "exp_binaire":
        return f"""
        {compilExpression(ast.children[2].value)}
        push rax 
        {compilExpression(ast.children[1].value)}
        pop rbx
        add rax, rbx
       """

def compilWhile(ast):
    global cpt 
    cpt +=1
    return f"""
        loop_start{cpt}: {compilExpression(ast.children[0].value)}
cmp rax, 0
je loop_end{cpt}
{compilCommande(ast.children[1].value)}
jmp loop_start
loop_end{cpt};


"""
def compilCommande(ast):
    asmVar = ""
    if ast.data == "com_while":
        asmVar += com_while(ast[0], ast[1])


