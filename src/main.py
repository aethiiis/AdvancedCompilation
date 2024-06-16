import sys
import Parser
import Compile

def get_source(filename : str) -> str:
    """
    get the source code contained in filename
    """
    with open(filename, 'r') as file:
        return file.read()

def get_ast(file_content : str) :
    """
    get the ast from the source code
    """
    tree = Parser.parser.parse(file_content)

    return tree

def compile(ast) :
    """
    compile to assembly code
    """
    asmLines = Compile.compile(ast)
    return asmLines

def save(asm, filename : str):
    """
    save assembly code to some filename
    """
    with open(filename, 'w') as fp:
        fp.write(asm)
    pass

if __name__ == "__main__":
    #ast = get_ast(get_source(sys.argv[1]))
    t = Parser.parser.parse(get_source("./test/exemple2.txt"))
    Parser.pretty_print(t)

    ast = get_ast(get_source("./test/exemple2.txt"))
    asm = compile(ast)
    #save(asm, sys.argv[2])
    save(asm, "compile.asm")
   # print(ast.pretty())
    
  
    # print(compile(ast))
    # print("Done")
    pass