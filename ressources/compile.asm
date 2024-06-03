extern printf, atoi
global main

section .data
long_format: db "%lld", 10, 0
argc: dd 0
argv: dd 0x: dq 0x2: dq 0

section .text
main:
push rbp
mov [argc], rdi
mov [argv], rsi
    
mov rbx, [argv]
mov rdi, [rbx + 8*(0+1)]
xor rax, rax
call atoi
mov [x], rax

mov rbx, [argv]
mov rdi, [rbx + 8*(1+1)]
xor rax, rax
call atoi
mov [x2], rax
