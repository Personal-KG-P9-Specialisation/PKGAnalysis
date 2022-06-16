import difflib, pandas as pd
import spacy

import warnings
warnings.filterwarnings('ignore')

#docker attach --detach-keys="ctrl-p" pkganalysis_analysis_1
# Assumes cskg source file in CSKG folder
def load_CSKG():
   df = pd.read_csv('CSKG/cskg.tsv',sep='\t', error_bad_lines=False)
   relations = set(df['relation'])
   node1s = set(df['node1'])
   node2s = set(df['node2'])
   nodes = list(node1s)
   nodes.extend(list(node2s))
   nodes = [x for x in nodes if x.startswith('/c/en')]
   return list(set(nodes)),relations

# Assumes conceptnet 5.5 / 5.7 source file in conceptnet folder
def load_ConceptNet5(path):
   # The graph is available at: https://github.com/commonsense/conceptnet5/wiki/Downloads
   # It will be downloaded as .csv but is tab-seperated
   df = pd.read_csv(path,sep='\t', error_bad_lines=False)
   relations = set(df.iloc[:,1])
   node1s = set(df.iloc[:,2])
   node2s = set(df.iloc[:,3])
   nodes = list(node1s)
   nodes.extend(list(node2s))
   nodes = [x for x in nodes if x.startswith('/c/en')]
   return list(set(nodes)), relations

# Assumes wikidata cs source file in wikidata folder
def load_WikidataCS():
   df = pd.read_csv('Wikidata/wikidata-cs-20200504.tsv',sep='\t', error_bad_lines=False)
   relations = set(df['relation'])
   node1s = set(df['node1;label'])
   node2s = set(df['node2;label'])
   nodes = list(node1s)
   nodes.extend(list(node2s))
   return list(set(nodes)),relations

def el2(em, nodelist, cutoff = 0.3):
   el_list = list()
   for node in nodelist:
       if em in str(node):
           el_list.append(node)
   return difflib.get_close_matches(em,el_list, cutoff=cutoff)
   
def el(em, nodelist):
   el_list = list()
   for node in nodelist:
       if em in node:
           el_list.append(node)
   return el_list

def load_conv():
   df = pd.read_csv('conv.tsv',sep='\t', error_bad_lines=False)
   nlp = spacy.load("en_core_web_md")
   nlp.add_pipe("entityLinker", last=True)
   
   utterances = list(df.iloc[:,1])
   spans = list()

   for utterance in utterances:
      doc = nlp(utterance)
      for entity in doc._.linkedEntities:
         spans.append(entity.get_span().text)
   return spans

def print_statistics(spans, nodes, cutoff=0.3):
   count = 0
   #spans = list(set(spans))
   for span in spans:
      matches = el2(span, nodes, cutoff=cutoff)
      if not matches:
         print(f"No match for: {span:>12}")
         count += 1
   print(f'Amount of No matches are:\t{count} of {len(spans)}\n')

"""if __name__ == "__main__":
   spans = load_conv()
   
   nodes1, _ = load_CSKG()
   print('---'*20,'\n')
   print('CSKG1\n')
   print_statistics(spans,nodes1)
   print('---'*20,'\n')

   print('ConceptNet 5.7\n')
   nodes2, _ = load_ConceptNet5('ConceptNet/conceptnet-assertions-5.7.0.csv')
   print_statistics(spans,nodes2)"""

"""print('---'*20,'\n')
   print('ConceptNet 5.5\n')
   nodes3, _ = load_ConceptNet5('ConceptNet/assertions5-5.tsv')
   print_statistics(spans,nodes3)
   print('---'*20,'\n')"""

"""print('WikidataCS\n')
   nodes, _ = load_WikidataCS()
   print_statistics(spans, nodes)  
   print('---'*20,'\n')"""
