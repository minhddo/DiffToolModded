import os


class Config:
    jar_path = 'jars'
    os.makedirs(jar_path, exist_ok=True)

    gumtree_cmd = ['java', '-jar', 'jars/ast_extractor_treesitter.jar']
