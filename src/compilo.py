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

def compile(fichier:str):
    parser = lark.Lark(grammaire, start="programme")
    with open(fichier, "r") as f:
        t = parser.parse(f.read())
        print(t.pretty())
        arguments = t.children[0]
        body = t.children[1]
        resultat = t.children[2]
        with open("compile.asm", "w") as f:
            # PARTIE DECLARATION DES VARIABLES

            ### Fonctions externes
            f.write(external_functions())

            ### Main
            f.write(main())

            ### Variables
            f.write(variables(arguments))
            
            ### Programme
            f.write(programme())

            # PARTIE OPENING
            f.write(opening())
            # argc = number of arguments & argv = arguments

            # PARTIE INITIALISATION DES VARIABLES MAIN
            f.write(initialisation_variables(arguments))

            # PARTIE BODY

            # PARTIE RETURN

            # PARTIE CLOSING

def external_functions():
    return "extern printf, atoi\n"

def main():
    return "global main\n"

def variables(arguments):
    res = """
section .data
long_format: db \"%lld\", 10, 0
argc: dd 0
argv: dd 0"""
    for i, var in enumerate(arguments.children):
        res += f"""{var.value}: dq 0"""

    return res

def programme():
    return """

        section .text
        main:"""

def opening():
    return """
    push rbp
    mov [argc], rdi
    mov [argv], rsi
    """

def initialisation_variables(arguments):
    res = ""
    for i, var in enumerate(arguments.children):
        res += f"""
        mov rbx, [argv]
        mov rdi, [rbx + 8*({i}+1)]
        xor rax, rax
        call atoi
        mov [{var}], rax
        """
    return res

if __name__ == "__main__":
    compile("fichier")