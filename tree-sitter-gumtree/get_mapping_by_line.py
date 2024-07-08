import networkx as nx
import os
import json
import sys
from utils.parsers import cpp_parser, java_parser, python_parser, js_parser,\
    ast_diff

def neighbors_in(u, q, filter_func=None):
    ''' Get neighbor having edges into this node
    Parameters
    ----------
    u: str/int
    q: nx.MultiDiGraph
    filter_func: lambda u, v, k, data -> bool

    Returns
    ----------
    list(str)/list(int) (based on the node id) set in the original graph
    '''
    if filter_func is None:
        return list(set(list(u_n for u_n, _ in q.in_edges(u))))
    else:
        return list(set(list(u_n for u_n, _, k, e in q.in_edges(u, data=True,
                                                                keys=True)
                             if filter_func(u_n, u, k, e))))


def neighbors_out(u, q, filter_func=None):
    ''' Neighbors out (neighbors that this node have at least one edge to)
    Parameters
    ----------
    u: str/int
    q: nx.MultiDiGraph
    filter_func: lambda u, v, k, data -> bool
    Returns
    ----------
    list(str)/list(int) (based on the node id) set in the original graph
    '''
    if filter_func is None:
        return list(set(list(u_n for _, u_n in q.out_edges(u))))
    else:
        return list(set(list(u_n for _, u_n, k, e in q.out_edges(u, data=True,
                                                                 keys=True)
                             if filter_func(u, u_n, k, e))))


class GumtreeASTUtils:

    def build_nx_graph(ndicts):
        nx_ast = nx.MultiDiGraph()
        for ndict in sorted(ndicts, key=lambda x: x['id']):
            nx_ast.add_node(ndict['id'], ntype=ndict['type'],
                            token=ndict['label'], graph='ast',
                            start_line=ndict['range']['begin']['line'],
                            start_col=ndict['range']['begin']['col'],
                            end_line=ndict['range']['end']['line'],
                            end_col=ndict['range']['end']['col'],
                            status=0)

            # Hypo 1: NX always keep the order of edges between one nodes and all
            # others, so we can recover sibling from this
            if ndict['parent_id'] != -1:
                nx_ast.add_edge(
                    ndict['parent_id'], ndict['id'], label='parent_child')
        return nx_ast


class GumtreeBasedAnnotation:
    '''Gumtree-based annotation between differencing ASTs'''

    def get_non_inserted_ancestor(rev_map_dict, dst_n, nx_ast_dst):
        parents = neighbors_in(dst_n, nx_ast_dst)
        while(len(parents) > 0):
            parent = parents[0]
            if parent not in rev_map_dict:
                parents = neighbors_in(parent, nx_ast_dst)
            else:
                return parent

    def build_mapping_line(map_dict):
        ''' Statement-level annotation'''
        # Insert a place holder node for each
        nx_ast_src = GumtreeASTUtils.build_nx_graph(map_dict['srcNodes'])
        nx_ast_dst = GumtreeASTUtils.build_nx_graph(map_dict['dstNodes'])
        src_lines = sorted(list(set([nx_ast_src.nodes[n]['start_line']
                     for n in nx_ast_src.nodes()])))
        dst_lines = sorted(list(set([nx_ast_dst.nodes[n]['start_line']
                     for n in nx_ast_dst.nodes()])))

        # Find the largest eleemnt in line
        # nx_ast_src = add_placeholder_func(nx_ast_src)
        # Node post processing, recheck if token equal
        for n_s in nx_ast_src.nodes():
            if n_s in map_dict['mapping']:
                n_d = map_dict['mapping'][n_s]
                if nx_ast_src.nodes[n_s]['token'] != nx_ast_dst.nodes[n_d]['token']:
                    del map_dict['mapping'][n_s]
                    map_dict['deleted'].append(n_s)
                    map_dict['inserted'].append(n_d)

        rev_map_dict = {v: k for k, v in map_dict['mapping'].items()}
        linvalids = [n for n in nx_ast_dst.nodes()
                     if n not in map_dict['inserted'] and n not in rev_map_dict]
        map_dict['inserted'].extend(linvalids)

        line_isrts = []
        line_dels = []
        line_maps = {}
        for l in src_lines:
            largest_elm = max([n for n in nx_ast_src.nodes() if
                               (nx_ast_src.nodes[n]['start_line'] == l and
                               nx_ast_src.nodes[n]['end_line'] == l) or
                               nx_ast_src.nodes[n]['ntype'] == r'\n'],
                              key=lambda x: (
                                  nx_ast_src.nodes[x]['end_col'] -
                                  nx_ast_src.nodes[x]['start_col']))
            if largest_elm in map_dict['deleted']:
                line_dels.append(l)
            else:
                line_maps[l] = nx_ast_dst.nodes[map_dict['mapping'][
                    largest_elm]]['start_line']

        for l in dst_lines:
            largest_elm = max([n for n in nx_ast_dst.nodes() if
                               nx_ast_dst.nodes[n]['start_line'] == l and
                               nx_ast_dst.nodes[n]['end_line'] == l],
                              key=lambda x: (
                                  nx_ast_dst.nodes[x]['end_col'] -
                                  nx_ast_dst.nodes[x]['start_col']))
            if largest_elm in map_dict['inserted']:
                line_isrts.append(l)

        return {'mapping': line_maps, 'deleted': line_dels,
                'inserted': line_isrts}


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 post_process_script.py file1 file2 outfile")
    fp1 = sys.argv[1]
    fp2 = sys.argv[2]
    parser = cpp_parser
    if fp1.endswith('java'):
        parser = java_parser
    elif fp1.endswith('py'):
        parser = python_parser
    elif fp1.endswith('js'):
        parser = js_parser
    map_dict = GumtreeBasedAnnotation.build_mapping_line(
        ast_diff(fp1, fp2, parser)
    )
    json_str = json.dumps(map_dict, indent=4)
    if len(sys.argv) > 3:
        with open(sys.argv[3], 'w') as f:
            f.write(json_str)
    else:
        print(json_str)
