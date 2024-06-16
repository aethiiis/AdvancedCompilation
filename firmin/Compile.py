import lark
import Parser

cpt = 0

op2asm = {"+": "add rax, rbx", "-": "sub rax, rbx"}

def compile(ast):
    # print(ast.children[0].children[0])
    # print(ast.children[1].children[0])
    asmString = ""
    asmString += "extern printf, atol ;déclaration des fonctions externes\n"
    asmString += "global main ; declaration main\n"
    asmString += "section .data ; section des données\n"
    asmString += "long_format: db '%lld',10, 0 ; format pour les int64_t\n"
    asmString += "argc : dq 0 ; copie de argc\n"
    asmString += "argv : dq 0 ; copie de argv\n"
    for function in ast.children[0].children:
        print(function.children[3])
        asmVar, vars = variable_declaration(function.children[1])
        asmString += asmVar
        asmString += f"{function.children[0].value} :"
        asmString += "push rbp; Set up the stack. Save rbp\n"
        asmString += compilCommand(function.children[2])
        asmString += compilReturn(function.children[3])
        asmString += "pop rbp\n"
        asmString += "ret\n"
    
    if ast.children[1].data == "fonction_main":
        asmVar, vars = variable_declaration(ast.children[1].children[0])
        asmString += asmVar
        asmString += "section .text ; instructions\n"
        asmString += "main :"
        asmString += "push rbp; Set up the stack. Save rbp\n"
        asmString += "mov [argc], rdi\n"
        asmString += "mov [argv], rsi\n"
        asmString += initMainVar(ast.children[1].children[0])
        asmString += compilCommand(ast.children[1].children[1])
        asmString += compilReturn(ast.children[1].children[2])
        asmString += "pop rbp\n"
        asmString += "xor rax, rax\n"
        asmString += "ret\n"

    return asmString

def variable_declaration(ast) :
    asmVar = ""
    vars = set()
    if ast.data != "liste_vide":
        for child in ast.children:
            asmVar += f"{child.value}: dq 0\n"
            vars.add(child.value)
    return asmVar, vars

def initMainVar(ast):
    asmVar = ""
    if ast.data != "liste_vide":
        index = 0
        for child in ast.children:
            asmVar += "mov rbx, [argv]\n"
            asmVar += f"mov rdi, [rbx + { 8*(index+1)}]\n"
            asmVar += "xor rax, rax\n"
            asmVar += "call atol\n"
            asmVar += f"mov [{child.value}], rax\n"
            index += 1
    return asmVar

def compilReturn(ast):
    asm = compilExpression(ast)
    asm += "mov rsi, rax \n"
    asm += "mov rdi, long_format \n"
    asm += "xor rax, rax \n"
    asm += "call printf \n"
    return asm

def compilCommand(ast):
    asmVar = ""
    if ast.data == "com_while":
        asmVar = compilWhile(ast)
    elif ast.data == "com_if":
        asmVar = compilIf(ast)
    elif ast.data == "com_sequence":
        asmVar = compilSequence(ast)
    elif ast.data == "com_asgt":
        asmVar = compilAsgt(ast)
    elif ast.data == "com_printf":
        asmVar = compilPrintf(ast)
    elif ast.data == "com_vide":
        asmVar = ""
    # elif ast.data == "com_decla_tableau":
    #     asmVar = f"{ast.children[0].value}: dq {ast.children[1].value}\n"
    # elif ast.data == "com_assgt_tableau":
    #     asmVar = f"mov rax, {ast.children[2].value}\n"
    #     asmVar += f"mov [{ast.children[0].value} + rax*8], rax\n"
    elif ast.data == "com_appel":
        print(ast.children)
        if (len(ast.children) == 1):
            asmVar = f"mov rdi, [{ast.children[0].value}]\n"
        elif (len(ast.children) == 2):
            asmVar = f"mov rdi, [{ast.children[0].value}]\n"
            asmVar += f"mov rsi, [{ast.children[1].value}]\n"
        elif (len(ast.children) >= 3):
            print("Pas géré")
        asmVar += f"call {ast.children[0].value}\n"
        asmVar += f"mov [{ast.children[0].value}], rax\n"
    return asmVar

def compilWhile(ast):
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

def compilIf(ast):
    global cpt
    cpt += 1
    return f""" 
            {compilExpression(ast.children[0])}
            cmp rax, 0
            jz fin{cpt}
            {compilCommand(ast.children[1])}
            fin{cpt} :
        """

def compilSequence(ast):
    asm = ""
    for child in ast.children :
        asm +=compilCommand(child)
    return asm

def compilAsgt(ast):
    asm = compilExpression(ast.children[1])
    asm += f"mov [{ast.children[0].value}], rax \n"
    return asm

def compilPrintf(ast):
    asm = compilExpression(ast.children[0])
    asm += "mov rsi, rax \n"
    asm += "mov rdi, long_format \n"
    asm += "xor rax, rax \n"
    asm += "call printf \n"
    return asm

def compilExpression(ast):
    if ast.data == "exp_variable":
        return f"mov rax, [{ast.children[0].value}]\n"
    elif ast.data ==  "exp_nombre":
        return f"mov rax, {ast.children[0].value}\n"
    elif ast.data == "exp_binaire":
        return f"""
                {compilExpression(ast.children[2])}
                push rax
                {compilExpression(ast.children[0])}
                pop rbx
                {op2asm[ast.children[1].value]}
                """
    return ""

if __name__ == "__main__":
    t = Parser.parser.parse("""
                fonction1(x,y){
                    var t1[4];
                    t1[0] = 1;
                    return (x+y);
                }
                fonction2(x,y){
                    return (x-y);
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
    print(Parser.pretty_print(t))
    print(compile(t))