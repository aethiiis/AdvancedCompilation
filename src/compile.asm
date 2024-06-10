extern printf, atol ;déclaration des fonctions externes
global main ; declaration main
section .data ; section des données
long_format: db '%lld',10, 0 ; format pour les int64_t
argc : dq 0 ; copie de argc
argv : dq 0 ; copie de argv
t1 : dq 0,0,0
t2 : dq 0,0,0,0
t3 : dq 3, 18
x : dq 0
section .text ; instructions
main :
push rbp; Set up the stack. Save rbp
mov rbp, rsp; Set up the stack. Set rbp to rbpmov [argc], rdi
mov [argv], rsi
lea rsi, [t3]
mov rax, [rsi + 0 ]
mov [x], rax 
mov rax, [x]
mov rsi, rax 
mov rdi, long_format 
xor rax, rax 
call printf 
mov rax, [x]
pop rbp
xor rax, rax
ret
