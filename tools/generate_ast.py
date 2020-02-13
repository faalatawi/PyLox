# Copyright (c) 2020 Faisal Alatawi. All rights reserved
# Using this source code is governed by an MIT license
# you can find it in the LICENSE file.

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
\tdef accept(self, visitor):
\t\treturn visitor.visit{class_name}(self)
"""
def defineAst(output_file, base_name, grammer):
    base = f"""# Copyright (c) 2020 Faisal Alatawi. All rights reserved
# Using this source code is governed by an MIT license
# you can find it in the LICENSE file. 

class {base_name}:
    pass
"""
    output_file.write(base)

    for k, v in grammer.items():
        output_file.write(defineType(k, base_name, v))
    
    output_file.close()


if __name__ == "__main__":
    path = "lox/grammer2.py"

    grammer = {   
            "Binary"   : ["left", "operator", "right"],
            "Grouping" : ["expression"],                      
            "Literal"  : ["value"],                         
            "Unary"    : ["operator","right"]
        }
    base_name = "Expr"
    
    with open(path, "w+") as output_file:
        defineAst(output_file, base_name, grammer)