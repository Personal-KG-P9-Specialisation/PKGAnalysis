import json

def listToString(s): 
    str1 = "" 
    for ele in s: 
        str1 += ele  
    return str1

def possesive_pronouns(content):
    rank = 0
    rank += content.count(" my ")
    rank += content.count(" your ")
    rank += content.count(" his ")
    rank += content.count(" her ")
    rank += content.count(" its ")
    rank += content.count(" our ")
    rank += content.count(" their ")
    return rank

def ownership_relation(content):
    relations = ["have", "own", "posses", "keep", "retain", "am", "are"]
    rank = 0
    if ("i " or "we ") in content:
        for relation in relations:
            rank += content.count(relation)
    return rank

def preference_relation(content):
    relations = ["like", "prefer", "love", "desire", "fancy", "enjoy", "appreciate", "admire", "cherish"]
    rank = 0
    if ("i " or "we ") in content:
        for relation in relations:
            rank += content.count(relation)
    return rank

def aversion_relation(content):
    relations = ["hate", "loath", "despise", "dislike", "resent", "detest", "dissaprove", "deprecate"]
    rank = 0
    if ("i " or "we ") in content:
        for relation in relations:
            rank += content.count(relation)
    return rank

def rank_data(conv_data, output_dir):
    with open(conv_data, 'r') as json_file:
        json_list = list(json_file)

    i = 1
    for json_str in json_list:
        result = json.loads(json_str)
        content = ""
        rank = 0

        for ele in result['dialog']:
            for text in ele:
                tmp = text['text'].split("\n")
                rank += ownership_relation(tmp[-1])
                rank += preference_relation(tmp[-1])
                rank += aversion_relation(tmp[-1])
                content = content + tmp[-1] + "\n"
        
        rank += possesive_pronouns(content)
        filename = output_dir + str(rank) + 'conv' + str(i) + '.txt'
        if rank != 0:
            with open(filename, 'w') as f:
                f.write(content)
            i += 1


if __name__ == "__main__":
    rank_data('/home/test/Github/PKGAnnotationSystem/personachat/personachat_combined.jsonl', '/home/test/Github/PKGAnnotationSystem/convs/')

