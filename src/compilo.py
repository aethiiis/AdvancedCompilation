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

with open("compile.asm", "w") as f:
    # PARTIE DECLARATION DES VARIABLES

    ### Fonctions externes
    f.write("extern printf, atoi\n")

    ### Main
    f.write("global main\n")

    ### Variables
    f.write("""
            section .data
            long_format: db \"%lld\", 10, 0
            argc: dd 0
            argv: dd 0
            i: dq 0
            liste_variables: dd 0
            """)
    for var in variables.children:
        f.write(f"""{var.value}: dq 0
                mov [{var.value}], rax
                """)

    ### Programme
    f.write("""
            section .text
            main:
            """)

    # PARTIE OPENING
    f.write("""
            push rbp
            mov [argc], rdi
            mov [argv], rsi
            """)
    # argc = number of arguments & argv = arguments

    # PARTIE INITIALISATION DES VARIABLES MAIN
    f.write(f"""
            debut_initialisation: nop
            cmp [argc], [i]
            je .fin_initialisation
            mov rax, [i]
            mov rbx, [argv]
            mov rdi, [rbx + 8*(rax+1)]
            inc rax
            mov [i], rax
            xor rax, rax
            call atoi
            mov [{variables.children}], rax
            jmp debut_initialisation
            """, )
    # PARTIE BODY

    # PARTIE RETURN

    # PARTIE CLOSING