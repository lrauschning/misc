#!/usr/bin/python3
import itertools
from collections import Counter

k = 1
q = 'HARFYAAQIVLHARFYAAQIVL'
t = 'VDMAAQIA'

q_tup = {}
for i in range(len(q) - k + 1):
    act_tuple_db = q[i:i + k]
    if act_tuple_db in q_tup.keys():
        q_tup[act_tuple_db].append(i)
    else:
        q_tup[act_tuple_db] = [i]

offset_list = {}
for i in range(len(t) - k + 1):
    act_tuple_query = t[i:i + k]
    if act_tuple_query in q_tup.keys():
        if act_tuple_query in offset_list.keys():
            list = [element - i for element in q_tup[act_tuple_query]]
            offset_list[act_tuple_query] += list
        else:
            list = [element - i for element in q_tup[act_tuple_query]]
            offset_list[act_tuple_query] = list


for key in offset_list.keys():
    print(f'{key}\t{offset_list[key]}')


offset_vector = Counter(itertools.chain(*offset_list.values()))
offset_vector_idx = [i for i in range(-len(t) + k, len(q) - k + 1)]
print(',\t'.join([str(i) for i in offset_vector_idx]))
print(',\t'.join([str(i) for i in [offset_vector[i] if i in offset_vector.keys() else 0 for i in offset_vector_idx]]))
