import difflib, pandas as pd

#assumes cskg source file in CSKG folder
def load_CSKG():
   df = pd.read_csv('CSKG/cskg.tsv',sep='\t', error_bad_lines=False)
   relations = set(df['relation'])
   node1s = set(df['node1'])
   node2s = set(df['node2'])
   nodes = list(node1s)
   nodes.extend(list(node2s))
   return nodes,relations


def el2(em, nodelist):
   el_list = list()
   for node in nodelist:
       if em in node:
           el_list.append(node)
   return difflib.get_close_matches(em,el_list, cutoff=0.3)
   
def el(em, nodelist):
   el_list = list()
   for node in nodelist:
       if em in node:
           el_list.append(node)
   return el_list

