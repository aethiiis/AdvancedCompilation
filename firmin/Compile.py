import lark
import Parser

cpt = 0

op2asm = {"+": "add rax, rbx", "-": "sub rax, rbx"}

variables = {}

def compile(ast):
    asmString = ""
    asmString += "extern printf, atol ;déclaration des fonctions externes\n"
    asmString += "global start ; entry point\n"
    asmString += "section .data ; section des données\n"
    asmString += "long_format: db '%lld',10, 0 ; format pour les int64_t\n"
    asmString += "argc : dq 0 ; copie de argc\n"
    asmString += "argv : dq 0 ; copie de argv\n"

    #asmString += variable_declaration(ast) # variables globales

    asmString += "section .text ; instructions\n"
    asmString += "start:\n"
    asmString += "push rbp\n"
    asmString += "mov rbp, rsp\n"
    asmString += "mov [argc], rdi\n"
    asmString += "mov [argv], rsi\n"
    
    # Push arguments for main function
    main_func = ast.children[1]
    index = 2
    for param in main_func.children[0].children:
        asmString += f"mov rax, [argv + {8 * index}]\n"
        asmString += "push rax\n"
        index += 1
    
    asmString += "call main\n"
    asmString += "xor rax, rax\n"
    asmString += "pop rbp\n"
    asmString += "ret\n"

    analyze_variables(ast)  # Perform the preliminary analysis
    print(variables)

    for function in ast.children[0].children:
        asmString += compile_function(function)

    asmString += compile_main(ast.children[1])
    return asmString

def analyze_variables(ast):
    global variables

    # Regular functions
    for func in ast.children[0].children:
        #print(func.pretty())
        func_name = func.children[0].value
        func_vars = {}
        index = 1
        # Process parameters
        for param in func.children[1].children:
            func_vars[param.children[0].value] = 8 * (index + 1)
            index += 1
        # Process local variables
        offset = -8
        analyze_command(func.children[2], func_vars, offset)
        variables[func_name] = func_vars
    
    # Main function
    print(ast.children[1].children[1])
    func_name = "main"
    func_vars = {}
    index = 1
    for param in ast.children[1].children[0].children:
            func_vars[param.children[0].value] = 8 * (index + 1)
            index += 1
    offset = -8
    analyze_command(ast.children[1].children[1], func_vars, offset)
    variables[func_name] = func_vars

def analyze_command(command, func_vars, offset):
    if command.data == "com_sequence":
        for sub_command in command.children:
            offset = analyze_command(sub_command, func_vars, offset)
    elif command.data == "com_asgt":
        var_name = command.children[0].value
        if var_name not in func_vars:
            func_vars[var_name] = offset
            offset -= 8
    elif command.data == "com_appel":
        var_name = command.children[0].value
        if var_name not in func_vars:
            func_vars[var_name] = offset
    elif command.data in ("com_while", "com_if"):
        for child in command.children:
            if isinstance(child, lark.Tree):
                offset = analyze_command(child, func_vars, offset)
    return offset

def variable_declaration(ast):
    asmVar = ""
    for func in ast.children[0].children + [ast.children[1]]:
        if func.children[1].data != "liste_vide":
            for child in func.children[1].children:
                if isinstance(child, lark.Token):
                    asmVar += f"{child.value}: dq 0\n"
    return asmVar

def compile_function(func):
    func_name = func.children[0].value
    asmString = f"{func_name}:\n"
    asmString += "push rbp ; Save rbp\n"
    asmString += "mov rbp, rsp ; Set up stack frame\n"
    asmString += compile_body(func_name, func.children[2])
    asmString += compile_return(func_name, func.children[3])
    asmString += "pop rbp\n"
    asmString += "ret\n"
    return asmString

def compile_main(func):
    asmString = "main:\n"
    asmString += "push rbp ; Save rbp\n"
    asmString += "mov rbp, rsp ; Set up stack frame\n"
    asmString += compile_body("main", func.children[1])
    asmString += compile_return("main", func.children[2])
    asmString += "pop rbp\n"
    asmString += "ret\n"
    return asmString

def compile_body(func_name, body):
    asm = ""
    for command in body.children:
        asm += compilCommand(func_name, command)
    return asm

def compile_return(func_name, ret_expr):
    asm = compilExpression(func_name, ret_expr)
    asm += "mov rsi, rax \n"
    asm += "mov rdi, long_format \n"
    asm += "xor rax, rax \n"
    asm += "call printf \n"
    return asm

def compilCommand(func_name, ast):
    asmVar = ""
    if ast.data == "com_while":
        asmVar = compilWhile(func_name, ast)
    elif ast.data == "com_if":
        asmVar = compilIf(func_name, ast)
    elif ast.data == "com_sequence":
        asmVar = compilSequence(func_name, ast)
    elif ast.data == "com_asgt":
        asmVar = compilAsgt(func_name, ast)
    elif ast.data == "com_printf":
        asmVar = compilPrintf(func_name, ast)
    elif ast.data == "com_vide":
        asmVar = ""
    elif ast.data == "com_appel":
        asmVar = compilAppel(func_name, ast)
    return asmVar

def compilWhile(func_name, ast):
    global cpt
    cpt += 1
    return f"""
            loop{cpt}:
                {compilExpression(func_name, ast.children[0])}
                cmp rax, 0
                jz fin{cpt}
                {compilCommand(func_name, ast.children[1])}
                jmp loop{cpt}
            fin{cpt}:
        """

def compilIf(func_name, ast):
    global cpt
    cpt += 1
    return f"""
            {compilExpression(func_name, ast.children[0])}
            cmp rax, 0
            jz else{cpt}
            {compilCommand(func_name, ast.children[1])}
            jmp fin{cpt}
            else{cpt}:
            {compilCommand(func_name, ast.children[2])}
            fin{cpt}:
        """

def compilSequence(func_name, ast):
    asm = ""
    for child in ast.children:
        asm += compilCommand(func_name, child)
    return asm

def compilAsgt(func_name, ast):
    asm = compilExpression(func_name, ast.children[1])
    if variables[func_name][ast.children[0].value] < 0:
        asm += f"mov [rbp{variables[func_name][ast.children[0].value]}], rax \n"
    else:
        asm += f"mov [rbp+{variables[func_name][ast.children[0].value]}], rax \n"
    return asm

def compilPrintf(func_name, ast):
    asm = compilExpression(func_name, ast.children[0])
    asm += "mov rsi, rax \n"
    asm += "mov rdi, long_format \n"
    asm += "xor rax, rax \n"
    asm += "call printf \n"
    return asm

def compilAppel(func_name, ast):
    asm = ""
    args = ast.children[2].children
    for arg in args:
        asm += compilExpression(func_name, arg)
        asm += f"push rax\n"
    asm += f"call {ast.children[1].value}\n"
    if variables[func_name][ast.children[0].value] < 0:
        asm += f"mov [rbp{variables[func_name][ast.children[0].value]}], rax\n"
    else:
        asm += f"mov [rbp+{variables[func_name][ast.children[0].value]}], rax\n"
    asm += f"add rsp, {8 * len(args)} ; Clean up stack\n"
    return asm

def compilExpression(func_name, ast):
    if ast.data == "exp_variable":
        if variables[func_name][ast.children[0].value] < 0:
            return f"mov rax, [rbp{variables[func_name][ast.children[0].value]}]\n"
        else:
            return f"mov rax, [rbp+{variables[func_name][ast.children[0].value]}]\n"
    elif ast.data == "exp_nombre":
        return f"mov rax, {ast.children[0].value}\n"
    elif ast.data == "exp_binaire":
        return f"""
                {compilExpression(func_name, ast.children[2])}
                push rax
                {compilExpression(func_name, ast.children[0])}
                pop rbx
                {op2asm[ast.children[1].value]}
                """
    return ""

if __name__ == "__main__":
    t = Parser.parser.parse("""
                fonction1(y, z){
                    x = 10;
                    u = 20;
                    while(y) {
                        printf(y);
                        z = fonction2(x, y);
                    }
                    return (x + y);
                }
                fonction2(x, y){
                    return (x - y);
                }
                main(x, y){
                    while(x) {
                       y = y + 1;
                       z = fonction1(x, y);
                       printf(z);
                    }
                    return (y);
                }
            """)
    print(Parser.pretty_print(t))
    print(compile(t))
