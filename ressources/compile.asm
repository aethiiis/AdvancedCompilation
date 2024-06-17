extern printf, atol ;déclaration des fonctions externes
global _start ; entry point
section .data ; section des données
long_format: db '%lld',10, 0 ; format pour les int64_t
argc : dq 0 ; copie de argc
argv : dq 0 ; copie de argv
section .text ; instructions
_start:
push rbp
mov rbp, rsp
mov [argc], rdi
mov [argv], rsi
mov rax, [argv + 16]
push rax
mov rax, [argv + 24]
push rax
call main
xor rax, rax
pop rbp
ret
fonction1:
push rbp ; Save rbp
mov rbp, rsp ; Set up stack frame

            loop1:
                mov rax, [rbp+24]

                cmp rax, 0
                jz fin1
                mov rax, [rbp+24]
mov rsi, rax 
mov rdi, long_format 
xor rax, rax 
call printf 
mov rax, [rbp+16]
push rax
mov rax, [rbp+24]
push rax
call fonction2
mov [rbp-8], rax
add rsp, 16 ; Clean up stack

                jmp loop1
            fin1:
        
                mov rax, [rbp+24]

                push rax
                mov rax, [rbp+16]

                pop rbx
                add rax, rbx
                mov rsi, rax 
mov rdi, long_format 
xor rax, rax 
call printf 
pop rbp
ret
fonction2:
push rbp ; Save rbp
mov rbp, rsp ; Set up stack frame

                mov rax, [rbp+24]

                push rax
                mov rax, [rbp+16]

                pop rbx
                sub rax, rbx
                mov rsi, rax 
mov rdi, long_format 
xor rax, rax 
call printf 
pop rbp
ret
main:
push rbp ; Save rbp
mov rbp, rsp ; Set up stack frame

                mov rax, 1

                push rax
                mov rax, [rbp+24]

                pop rbx
                add rax, rbx
                mov [rbp+24], rax 
mov rax, [rbp+16]
push rax
mov rax, [rbp+24]
push rax
call fonction1
mov [rbp-8], rax
add rsp, 16 ; Clean up stack
mov rax, [rbp-8]
mov rsi, rax 
mov rdi, long_format 
xor rax, rax 
call printf 
mov rax, [rbp+24]
mov rsi, rax 
mov rdi, long_format 
xor rax, rax 
call printf 
pop rbp
ret
