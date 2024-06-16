import lark # type: ignore

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

def compile(fichier:str) -> None:
    parser = lark.Lark(grammaire, start="programme")
    with open(fichier, "r") as f:
        t = parser.parse(f.read())
        print(t.pretty())
        arguments = t.children[0]
        body = t.children[1]
        resultat = t.children[2]
        with open("ressources/compile.asm", "w") as f:
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
            f.write(compilCommand(body))

            # PARTIE RETURN
            f.write(compilReturn(resultat))

            # PARTIE CLOSING
            f.write(closing())

def external_functions() -> str:
    return "extern printf, atoi\n"

def main():
    return "global main\n"

def variables(arguments) -> str:
    res = """
section .data
long_format: db \"%lld\", 10, 0
argc: dd 0
argv: dd 0"""
    for i, var in enumerate(arguments.children):
        res += f"""{var.value}: dq 0"""

    return res

def programme() -> str:
    return """

section .text
main:"""

def opening() -> str:
    return """
push rbp
mov [argc], rdi
mov [argv], rsi
    """

def initialisation_variables(arguments) -> str:
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

def compilBody(ast) -> str:
    pass

def compilCommand(ast) -> str:
    asmVar = ""
    if ast.data == "com_while":
        asmVar = compilWhile(ast)
    elif ast.data == "com_if":
        asmVar = compilIf(ast)
    elif ast.data == "com_sequence":
        asmVar = compilSequence(ast)
    elif ast.data == "com_print":
        asmVar = compilPrintf(ast)
    elif ast.data == "com_asgt":
        asmVar = compilAffectation(ast)

def compilWhile(ast) -> str:
    global cpt
    cpt += 1
    return f"""
loop{cpt} : {compilExpression(ast.children[0])}
cmp rax, 0
jz fin{cpt}
{compilCommand(ast.children[1])}
jmp loop{cpt}
fin{cpt} :
"""

def compilIf(ast) -> str:
    global cpt
    cpt += 1
    return f"""
{compilExpression(ast.children[0].value)}
cmp rax, 0
jz fin{cpt}
{compilCommand(ast.children[1].value)}
fin{cpt} :
"""

def compilPrintf(ast) -> str:
    asm = f"""
{compilExpression(ast.children[0])}
mov rsi, rax
mov rdi, fmt
xor rax, rax
call printf
"""
    return asm

def compilAffectation(ast) -> str:
    pass

def compilExpression(ast) -> str:
    if ast.data == "exp_variable":
        return f"mov rax, [{ast.value}]"

def compilReturn(ast) -> str:
    return compilPrintf(ast)

def compilSequence(ast) -> str:
    asm = ""
    for child in ast.children:
        asm += compilCommand(child)
    return asm

def closing() -> str:
    return """
pop rbp
xor rax, rax
ret
"""

if __name__ == "__main__":
    compile("ressources/fichier")