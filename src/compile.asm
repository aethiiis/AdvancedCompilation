extern printf, atol ;déclaration des fonctions externes
global main ; declaration main
section .data ; section des données
long_format: db '%lld',10, 0 ; format pour les int64_t
argc : dq 0 ; copie de argc
argv : dq 0 ; copie de argv
t1: dq 0
section .text ; instructions
main :push rbp; Set up the stack. Save rbp
mov [argc], rdi
mov [argv], rsi
mov rbx, [argv]
mov rdi, [rbx + 8]
xor rax, rax
call atol
mov [t1], rax
mov rax, 0
mov [X], rax 
mov rax, [y]
mov rsi, rax 
mov rdi, long_format 
xor rax, rax 
call printf 
pop rbp
xor rax, rax
ret
