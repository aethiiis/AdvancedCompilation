extern printf, atol ;déclaration des fonctions externes
global main ; declaration main
section .data ; section des données
long_format: db '%lld',10, 0 ; format pour les int64_t
argc : dq 0 ; copie de argc
argv : dq 0 ; copie de argv
t2 : dq 0,0,0,0
t2_size : dq 4
x : dq 0
section .text ; instructions
main :
push rbp; Set up the stack. Save rbp
mov rbp, rsp; Set up the stack. Set rbp to rbp
mov [argc], rdi
mov [argv], rsi
mov rax, 1
mov [t2 + 0], rax
mov rax, 5
mov [t2 + 8], rax

                mov rax, [t2 + 8 ]

                push rax
                mov rax, [t2 + 0 ]

                pop rbx
                add rax, rbx
                mov [x], rax 
mov rax, [x]
mov rsi, rax 
mov rdi, long_format 
xor rax, rax 
call printf 
pop rbp
xor rax, rax
ret
