"""
"""
import re
import os

def load_from_file(path):
    """
    - function: load and parsing file

    param:
    path(string) -- file's location
    
    return:
    rules(list of list) -- rule template
        (e.g. [[('#1', 'X', 'Y'), ('#2', 'X', 'Z'), ('#3', 'Z', 'Y'), 3],
               [('#1', 'X', 'Y'), ('#2', 'X', 'Y'), 3]])
    """
    with open(path, "r") as f:
        text = f.readlines()
        text = [x for x in text if not x.startswith("%") and x.strip() != ""]
        text = "".join(text)
        rules = [x for x in re.split("\.\n|\.\Z", text) if x != "" and
                 x != "\n" and not x.startswith("%")]
        rules = parse_rules(rules)
        return rules
    
def parse_rules(rules):
    """
    - function: load rule template and parsing using regular expression
    
    param:
    rules(list of strings) -- (such as ['2\t#1(X, Y) :- #2(X, Z),#3(Z, Y)'])

    return:
    parsed_rules(list of lists) -- (such as [('#1', 'X', 'Y'), ('#2', 'X', 'Z'), ('#3', 'Z', 'W'), ('#4', 'W', 'Y'), 2])
    max_atom(int) -- Maximum number of rule components for all rules
    """
    parsed_rules = []
    max_atom = 0
    for rule in rules:
        num = rule[:rule.find('\t')]
        rule = re.findall(r'#\d+\(.*?\)', rule)
        listAtoms = [re.split('[(),]', item)[:-1] for item in rule ]
        atoms = [(pred, sub, obj.strip()) for [pred, sub, obj] in listAtoms]
        max_atom = max(max_atom, len(atoms))
        atoms.append(int(num))
        parsed_rules.append(atoms)
       
    return parsed_rules, max_atom

def load_conf(path):
    """
    - function: read config file

    param:
    path(string) -- config file path

    return:
    conf -- config (dictionary)
    """
    file_name = path.split("/")[-1]

    with open(path, 'r') as f:
        conf = eval(f.read())
    return conf

def create_directory(directory): 
    """
    -function: create a directory if it doesn't exist

    param:
    directory(string) -- file's location (directory)
    """
    try: 
        if not os.path.exists(directory): 
            os.makedirs(directory) 
    except OSError: 
        print("Error: Failed to create the directory.")
        