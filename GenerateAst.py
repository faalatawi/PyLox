import sys

# xx = f"""x = {12+13}
# this is easy"""

# print(xx)


def new_class(class_name, base_name, constr_args, constr_body, visit_type ):
    return f"""
class {class_name}({base_name}):
def __init__(self, {constr_args}):
    {constr_body}

def accept(self, visitor):
    return visitor.{visit_type}(self)
"""

if __name__ == "__main__":
    arg_length = len(sys.argv)
    if arg_length != 3:
        print("Usage: generate_ast [output directory]")
        exit(2)        
    
    path = sys.argv[2]
    runFile(path)