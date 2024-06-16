# Compilation d'un Fichier ASM avec NASM et GCC

Ce guide vous explique comment compiler un fichier assembleur (`.asm`) en utilisant NASM (Netwide Assembler) et GCC (GNU Compiler Collection).

## Prérequis

Avant de commencer, assurez-vous d'avoir les outils suivants installés sur votre système :

1. **NASM** : Assembleur pour le langage assembleur x86.
2. **GCC** : Collection de compilateurs pour divers langages de programmation, y compris le C.

### Installation de NASM et GCC

#### Sur Ubuntu / Debian


nasm -f elf64 compile.asm -o compile.o

gcc -no-pie compile.o -o main

./main
