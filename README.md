# Compilateur nanoC de A à Z

Ce guide vous explique comment compiler un fichier assembleur (`.asm`) en utilisant NASM (Netwide Assembler) et GCC (GNU Compiler Collection).

## Prérequis

Avant de commencer, assurez-vous d'avoir les outils suivants installés sur votre système :

1. **NASM** : Assembleur pour le langage assembleur x86.
2. **GCC** : Collection de compilateurs pour divers langages de programmation, y compris le C.
3. Pour plus de facilité, il convient de se placer dans le répertoire src via la commande cd src

## Générer le fichier assembleur

Pour générer le fichier assembleur, il suffit d'exécuter le fichier main.py suivi de 
1. le chemin relatif du fichier que l'on veut parser (par exemple : ./test/exemple1.txt si l'on se trouve dans src)
2. le chemin relatif du fichier où l'on veut générer le code assembleur (par exemple : compile.asm)


## Compiler le fichier assembleur


nasm -f elf64 compile.asm -o compile.o

gcc -no-pie compile.o -o main

./main

Le cas écheant, on insère les arguments à la suite du ./main
