import sys

# grammer = {   "Binary"   : [("Expr","left"), ("Token", "operator"), ("Expr", "right")],
#             "Grouping" : [("Expr","expression")],                      
#             "Literal"  : [("Object", "value")],                         
#             "Unary"    : [("Token", "operator")], [("Expr", "right")]}

def defineType(class_name, base_name, args):
    
    if len(args) > 1:
        constr_args = ", ".join(args)
    else:
        constr_args = args[0]
    
    constr_body = ""

    for a in args :
        constr_body += f"\t\tself.{a} = {a} \n"

    return f"""\n
class {class_name}({base_name}):
\tdef __init__(self, {constr_args}):
{constr_body}
"""
# def accept(self, visitor):
#     return visitor.{visit_type}(self)

def defineAst(output_file, base_name, grammer):
    base = f"""

class {base_name}:
    pass

"""
    output_file.write(base)

    for k, v in grammer.items():
        output_file.write(defineType(k, base_name, v))
    
    output_file.close()


if __name__ == "__main__":
    # arg_length = len(sys.argv)
    # if arg_length != 3:
    #     print("Usage: generate_ast [output directory]")
    #     exit(2)        
    
    # path = sys.argv[2]
    # runFile(path)

    path = "grammer.py"

    grammer = {   
            "Binary"   : ["left", "operator", "right"],
            "Grouping" : ["expression"],                      
            "Literal"  : ["value"],                         
            "Unary"    : ["operator","right"]
        }
    base_name = "Expr"
    
    with open(path, "w+") as output_file:
        defineAst(output_file, base_name, grammer)