"""
data filtering
	- proof path가 없는 데이터 제거
"""
import copy
import random
import torch
import numpy as np
from torch.utils.data import Dataset
from collections.abc import Iterable

class proof_path_dataset(Dataset): 
    def __init__(self, relation_tensor, rule_temp_tensor, label, augment_num, KG, neg_per_pos, 
                 id2sym_dict, sym2id_dict, unify_dict):
        
        self.relation_tensor = relation_tensor
        self.rule_temp_tensor = rule_temp_tensor
        self.augment_num = augment_num
        self.KG_relation = set(KG['pred'])
        self.neg_per_pos = neg_per_pos
        self.id2sym_dict = id2sym_dict
        self.unify_dict = unify_dict
        self.sym2id_dict = sym2id_dict
        self.label = label

    def __len__(self): 
        return len(self.relation_tensor)

    def __getitem__(self, idx): 
        rel_path = self.relation_tensor[idx]
        rule_template= self.rule_temp_tensor[idx]
        label = self.label
        return rel_path, rule_template, label

def negative_samplig(rel_path, rule_tamplate, KG_relation, augment_num, neg_per_pos, 
                     sym2id_dict, id2sym_dict, unify_dict):

    pos_neg_rel_path = copy.deepcopy(rel_path)
    pos_neg_rule_path = copy.deepcopy(rule_tamplate)
    for _ in range(neg_per_pos):
        for p_id, path in enumerate(rel_path):
            neg_path = []
            neg_rule = []
            if path[0][0] != sym2id_dict['PAD']: 
                for rule_relation_idx in rule_tamplate[p_id][0]:
                    rule_relation = '_'.join(id2sym_dict[rule_relation_idx].split('_')[:-1])
                    neg_pred = list(KG_relation - unify_dict[rule_relation])

                    if len(neg_pred) == 0:
                        neg_path.append(sym2id_dict['PAD'])
                        neg_rule.append(sym2id_dict['UNK'])
                    else:
                        neg_path.append(sym2id_dict[random.choice(neg_pred)])
                        neg_rule.append(rule_relation_idx)
                neg_path = [neg_path for _ in range(augment_num)]
                neg_rule = [neg_rule for _ in range(augment_num)]

            pos_neg_rel_path.append(neg_path)
            pos_neg_rule_path.append(neg_rule)

    return pos_neg_rel_path, pos_neg_rule_path


def flatten(iter_object):

    for element in iter_object:
        if isinstance(element, Iterable):
            yield from flatten(element)
        else:
            yield element
            

def data_filter(path_to_query):

    path_existence = True
    if len(list(flatten(path_to_query))) == 0:
        path_existence = False
    return path_existence


def add_pad_token(rel_path_to_template, max_atom, sym2id_dict):

    for path_idx, rel_path in enumerate(rel_path_to_template):
        rel_path_to_template[path_idx] = list(map(lambda x : 
                                                  x + [sym2id_dict['PAD']]*(max_atom-len(rel_path[0])), rel_path))
    return rel_path_to_template


def padding(relation_path, rule_temp_path, rules, max_path, max_atom, neg_per_pos, sym2id_dict):
    """
    - function: Padding all proof paths with the maximum number of components and the maximum number of paths

    param:
    relation_path -- Set of unified KG relation paths for all query triples
        (e.g. if given Query triple = [nationality BART, USA] and Rule template = [#1(X, Y) :- #2(X, Z), #3(Z, Y)]
              then KG relation path = ['nationaliy', 'birthPlace', 'locatedIn'])
    rule_temp_path -- Set of unified rule template relation paths for all query triples
        (e.g. if given Query triple = [nationality BART, USA] and Rule template = [#1(X, Y) :- #2(X, Z), #3(Z, Y)]
              then Rule template path = ['#1', '#2', '#3'])
    rules(list of list) -- all rule template 
        (e.g. [[('#1', 'X', 'Y'), ('#2', 'X', 'Z'), ('#3', 'Z', 'Y'), 3],
               [('#1', 'X', 'Y'), ('#2', 'X', 'Y'), 3]])
    max_path(int) -- Maximum number of proof paths for all queries
    max_atom(int) -- Maximum number of rule components for all rules
    neg_per_pos(int) -- the number of negative proof path to be sampled per positive proof path
    sym2id_dict(dictionary) -- a dictionary for mapping symbol-type relation to index
        (e.g. {'UNK': 0, 'PAD': 1, '#1_0_0': 2, ..., 'hasParent': 20, 'nationality': 21, ... })

    return:
    relation_path -- Padded relation_path
    rule_temp_path -- Padded rule_temp_path
    """   
    single_temp_size = 1 + (1 * neg_per_pos)
    for query_idx, (rel_path_to_query, rule_temp_path_to_query) in \
        enumerate(zip(relation_path, rule_temp_path)):
        rel_path_to_query = list(rel_path_to_query)
        rule_temp_path_to_query = list(rule_temp_path_to_query)
        
        for template_idx, (rel_path_to_template, rule_temp_path_to_template) in \
            enumerate(zip(rel_path_to_query, rule_temp_path_to_query)):
            if len(rel_path_to_template) == 0:
                padding = np.ones((max_path*single_temp_size, rules[template_idx][-1], max_atom), 
                                  dtype=int).tolist()
                rel_path_to_query[template_idx] = padding
                rule_temp_path_to_query[template_idx] = padding

            elif len(rel_path_to_template) != 0:
                pad_rel_path_to_template = []
                pad_rule_temp_path_to_template = []

                if rel_path_to_template[0] != max_atom:
                    rel_path_to_template = add_pad_token(rel_path_to_template, max_atom, sym2id_dict)
                    rule_temp_path_to_template = add_pad_token(rule_temp_path_to_template, max_atom, sym2id_dict)
                    
                num_pos_path = int(len(rel_path_to_template)/single_temp_size)
                for i in range(0, len(rel_path_to_template), num_pos_path):
                    pad_rel_path_to_template += rel_path_to_template[i:i+num_pos_path]
                    pad_rule_temp_path_to_template += rule_temp_path_to_template[i:i+num_pos_path]
                    padding = np.ones((max_path-num_pos_path, rules[template_idx][-1], max_atom),
                                      dtype=int).tolist()
                    pad_rel_path_to_template += padding
                    pad_rule_temp_path_to_template += padding
                
                rel_path_to_query[template_idx] = pad_rel_path_to_template
                rule_temp_path_to_query[template_idx] = pad_rule_temp_path_to_template
        relation_path[query_idx] = tuple(rel_path_to_query)
        rule_temp_path[query_idx] = tuple(rule_temp_path_to_query)
        
    return relation_path, rule_temp_path

def convert_list_to_tensor(path_data):
    
    path_tensor = []
    for i in path_data:
        for j in i:
            path_tensor.append(j)
    path_tensor = torch.tensor(path_tensor)
    return path_tensor