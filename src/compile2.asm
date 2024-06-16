extern printf ; déclaration de la fonction externe printf
global main ; déclaration de main
section .data ; section des données
long_format: db '%lld', 10, 0 ; format pour les int64_t
argc: dq 0 ; copie de argc
argv: dq 0 ; copie de argv
t2: dq 0, 0, 0, 0 ; déclaration du tableau t2
x: dq 0 ; déclaration de la variable x
section .text ; section des instructions
main:
    push rbp ; sauvegarde de rbp
    mov rbp, rsp ; initialisation de rbp
    mov [argc], rdi ; copie de argc
    mov [argv], rsi ; copie de argv
    
    ; Initialisation de t2[0] à 1
    mov rax, 1
    mov [t2], rax
    
    ; Initialisation de t2[1] à 5
    mov rax, 5
    mov [t2 + 8], rax
    
    ; Récupération de t2[0]
    mov rax, [t2] ; valeur de t2[0]
    mov [x], rax ; stockage de la valeur dans x
    
    ; Affichage de x
    mov rax, [x]
    mov rsi, rax
    mov rdi, long_format
    xor rax, rax
    call printf
    
    ; Retour de la valeur de x
    mov rax, [x]
    pop rbp ; restauration de rbp
    ret


    elif ast.data == "exp_len_tableau" :
        asm = f"mov rax, {ast.children[0].value}\n"
        global cpt_len
        asm += f""" 
            loop{cpt_len} : {compilExpression(ast.children[0])}
                cmp rax, 0
                jz fin{cpt}
                {compilCommand(ast.children[1])}
                jmp loop{cpt}
            fin{cpt} :
        """
        asm += "xor rax, rax"
        asm += "mov rax, rbx"