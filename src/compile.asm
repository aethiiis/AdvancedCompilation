extern printf, atol ;déclaration des fonctions externes
global main ; declaration main
section .data ; section des données
long_format: db '%lld',10, 0 ; format pour les int64_t
argc : dq 0 ; copie de argc
argv : dq 0 ; copie de argv
t1 : dq 3, 18
t1_size : dq 2
x : dq 0
y : dq 0
section .text ; instructions
main :
push rbp; Set up the stack. Save rbp
mov rbp, rsp; Set up the stack. Set rbp to rbp
mov [argc], rdi
mov [argv], rsi
mov rax, [t1 + 8 ]
mov [x], rax 
mov rax, [t1 + 0 ]
mov [y], rax 
mov rax, [x]
mov rsi, rax 
mov rdi, long_format 
xor rax, rax 
call printf 
mov rax, [y]
mov rsi, rax 
mov rdi, long_format 
xor rax, rax 
call printf 
pop rbp
xor rax, rax
ret
