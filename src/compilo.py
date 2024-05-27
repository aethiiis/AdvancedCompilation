import functions


with open("compile.asm", "w") as f:
    # PARTIE DECLARATION DES VARIABLES

    ### Fonctions externes
        f.write("extern printf, atoi\n")

        ### Main
        f.write("global main\n")

        ### Variables
        f.write("""
                section .data
                long_format: db \"%lld\", 10, 0
                argc: dd 0
                argv: dd 0
                i: dq 0
                liste_variables: dd 0
                """)
        for var in variables.children:
                f.write(f"""{var.value}: dq 0
                        mov [{var.value}], rax
                        """)

        ### Programme
        f.write("""
                section .text
                main:
                """)

        # PARTIE OPENING
        f.write("""
                push rbp
                mov [argc], rdi
                mov [argv], rsi
                """)
        # argc = number of arguments & argv = arguments
        i= 0
        # PARTIE INITIALISATION DES VARIABLES MAIN
        for child in variables.children: 
                f.write(f"""
                        mov rbx, [argv]\n
                        mov rdi, [rbx + 8*({i}+1)]\n
                        xor rax, rax\n
                        call atoi\n
                        mov [{child.value}], rax\n
                        """, )
                i += 1
        


    # PARTIE BODY

    # PARTIE RETURN

    # PARTIE CLOSING