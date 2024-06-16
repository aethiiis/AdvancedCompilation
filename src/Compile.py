import lark

cpt = 0

op2asm = {"+": "add rax, rbx", "-": "sub rax, rbx"}

cpt_tableau = 0

def compile(ast):
    asmString = ""
    asmString = asmString + "extern printf, atol ;déclaration des fonctions externes\n"
    asmString = asmString + "global main ; declaration main\n"
    asmString = asmString + "section .data ; section des données\n"
    asmString = asmString + "long_format: db '%lld',10, 0 ; format pour les int64_t\n"
    asmString = asmString + "argc : dq 0 ; copie de argc\n"
    asmString = asmString + "argv : dq 0 ; copie de argv\n"
  #  print(ast.children[0])
    asmVar, vars = variable_declaration(ast.children[0])
    
    for child in ast.children[1].children:
        asmString += localVariables(child)
        #print(child)
    asmString = asmString + asmVar
    asmString = asmString + "section .text ; instructions\n"
    asmString += "main :\n"
    asmString += "push rbp; Set up the stack. Save rbp\n"
    asmString += "mov rbp, rsp; Set up the stack. Set rbp to rbp\n"
    asmString += "mov [argc], rdi\n"
    asmString += "mov [argv], rsi\n"
    asmString += initMainVar(ast.children[0])
    asmString += compilCommand(ast.children[1])
    asmString += compilReturn(ast.children[2])
    asmString += "pop rbp\n"
    asmString += "xor rax, rax\n"
    asmString += "ret\n"
    return asmString

def variable_declaration(ast) :
    asmVar = ""
    vars = set()
    names = 0
    if ast.data != "liste_vide":
        for child in ast.children:
           # print(child)
          #  print(child[0] == "[")
            if (child[0] == "t"):
                position = child.find("[")+1
              #  print(position)
                varName = child[:position-1]
                decla = "0"
                taille = (int)(child[position])
                for i in range (taille-1):
                    decla += ",0"
                asmVar += f"{varName}: dq {decla}\n"
                asmVar+= f"{varName}_size : dq {taille}\n"
                vars.add(child.value)
            elif (child[0] == "["):
                tableau = eval(child)
              #  print(tableau)
                asmVar += f"t_ext{names}: dq "
                for element in tableau :
                    asmVar += f"{element}, "
                asmVar = asmVar[:-2]
                asmVar += "\n"
                names +=1
            else :
                asmVar += f"{child.value}: dq 0\n"
                vars.add(child.value)
            
    return asmVar, vars

def localVariables(ast):
    asmString = ""
    if(ast.data == ("com_decla_tableau")):
     #   print(ast.children[0])
        try :
            position = ast.children[0].find("[")-1
            varName = ast.children[0][:position+1]
            asm = f"{varName} : dq "
            ext_table = eval(ast.children[1])

            for i in range (len(ext_table)) :
                asm += f"{ext_table[i]}, "

            asm = asm[:-2]
            asmString += f"{asm}\n"
            asmString+= f"{varName}_size : dq {len(ext_table)}\n"
        except Exception as e :
            position = ast.children[0].find("[")-1
            varName = ast.children[0][:position+1]
            asm = f"{varName} : dq 0"
            table = ast.children[0]
            position = table.find("[")+1
            taille = (int)(table[position])
            for i in range (taille-1):
                asm += ",0"
            asmString += f"{asm}\n"
            asmString+= f"{varName}_size : dq {taille}\n"
    elif(ast.data == ("com_asgt")):
        asmString += f"{ast.children[0]} : dq 0\n"  
    return asmString
   
def initMainVar(ast):
    asmVar = ""
   # print("balba")
    if ast.data != "liste_vide":
       # print("balba1")
        index = 0
        for child in ast.children:
            if (child[0] == "t"):
               # print("balba2")
                asmVar += "mov rbx, [argv]\n"
                asmVar += f"mov rdi, [rbx + { 8*(index+1)}]\n"
                asmVar += "xor rax, rax\n"
                asmVar += "call atol\n"
                asmVar += f"mov [{child[:child.find('[')]}], rax\n"
                position = child.find("[")+1
                taille = (int)(child[position])
                index += taille
          #  elif (child[0] == "["):
            elif (child[0] == "["):
                tableau = eval(child)
            else:
              #  print("balba3")
                asmVar += "mov rbx, [argv]\n"
                asmVar += f"mov rdi, [rbx + { 8*(index+1)}]\n"
                asmVar += "xor rax, rax\n"
                asmVar += "call atol\n"
                asmVar += f"mov [{child.value}], rax\n"
                index += 1
    return asmVar

def compilReturn(ast):
    asm = ""
    for child in ast.children :
        asm += compilExpression(child)
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
    elif ast.data == "com_assgt_tableau":
        asmVar = compilAssgtTableau(ast)
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


    
def compilAssgtTableau(ast):
    asm = ""
    asm = compilExpression(ast.children[2])
    asm += f"mov [{ast.children[0]} + {8*(int)(ast.children[1])}], rax\n"
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
    elif ast.data == "access_table" :
        
        array_name = ast.children[0].value
        index = (int)(ast.children[1].children[0]) 
        asm = f"mov rax, [{array_name} + {8*index} ]\n"
        return asm

    elif ast.data == "exp_len_tableau" :
        name = ast.children[0].value
        asm = f"mov rax, [{name}_size]\n"
        return asm

    return ""