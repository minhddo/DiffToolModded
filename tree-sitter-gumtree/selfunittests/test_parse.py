from utils.draw_utils import ast_to_agraph
from utils.parsers import cpp_parser, python_parser, convert_to_nx, \
    convert_to_dict, ast_cat, ast_diff
import os


def test1():
    code = bytes(
        r'''#include <stdio.h>

    int main(int argc, char** argv){
        int a = 2;
        int b = 3;
        a = a + b;
        for (int i = 0; i < 3; i++){
            a += 1;
        }
        printf("Hello, World! %d\n", &a);
        return 0;
    }
    ''', 'utf-8')
    tree = cpp_parser.parse(code)
    nx_g = convert_to_nx(tree, code)
    os.makedirs('visualized_tests', exist_ok=True)
    ast_to_agraph(nx_g, 'visualized_tests/cpp_tree.png')
    line1_ns = [n for n in nx_g if nx_g.nodes[n]['start_line'] == 1]
    print(line1_ns)
    line1_cs = [nx_g.nodes[n]['token'] for n in line1_ns]
    print(line1_cs)


def test2():
    code = bytes(
        r'''
    import os
    a = 1
    b = 2
    a = a + b
    for i in range(3):
        a += 1
    print("Hello world {}".format(a))
    ''', 'utf-8')
    tree = python_parser.parse(code)
    nx_g = convert_to_nx(tree, code)
    os.makedirs('visualized_tests', exist_ok=True)
    ast_to_agraph(nx_g, 'visualized_tests/python_tree.png')
    line1_ns = [n for n in nx_g if nx_g.nodes[n]['start_line'] == 1]
    print(line1_ns)
    line1_cs = [nx_g.nodes[n]['token'] for n in line1_ns]
    print(line1_cs)

def test3():
    code = bytes(
        r'''#include <stdio.h>

    int main(int argc, char** argv){
        int a = 2;
        int b = 3;
        a = a + b;
        for (int i = 0; i < 3; i++){
            a += 1;
        }
        printf("Hello, World! %d\n", &a);
        return 0;
    }
    ''', 'utf-8')
    tree = cpp_parser.parse(code)
    out_dict = convert_to_dict(tree, code)
    print(out_dict)


def test4_astcat():
    fp1 = "selfunittests/file1.cpp"
    fp2 = "selfunittests/file2.cpp"
    cat_dict = ast_cat(fp1, fp2, cpp_parser)
    print(cat_dict)


def test5_astdiff():
    fp1 = "selfunittests/file1.cpp"
    fp2 = "selfunittests/file2.cpp"
    mapping_dict = ast_diff(fp1, fp2, cpp_parser)
    print(mapping_dict)


if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4_astcat()
    test5_astdiff()
