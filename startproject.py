import os
import argparse

def create_dir_structure(name):
    os.mkdir(f"{name}")
    os.mkdir(f"./{name}/database")
    os.mkdir(f"./{name}/routes")
    os.mkdir(f"./{name}/models")
    with open(f"./{name}/main.py",'w'): pass
    with open(f"./{name}/database/__init__.py",'w'): pass
    with open(f"./{name}/database/connection.py",'w'): pass
    with open(f"./{name}/routes/__init__.py",'w'): pass
    with open(f"./{name}/models/__init__.py",'w'): pass
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    args = parser.parse_args()
    create_dir_structure(args.name)