from subprocess import call
import spacy
from formatting import output_color
import requests
nlp = spacy.load("en_core_web_sm")
import json
import os

VERBOSE = 0
def load_txt_data():
    # try :
    path_file_ner = os.path.normpath(os.path.dirname(__file__) + os.sep + os.pardir)
    path_file_ner = os.path.join(path_file_ner, "Data-cache")
    path_file_ner = os.path.join(path_file_ner, "questiontext.json")
    data = json.load(open(path_file_ner, encoding="utf-8"))
    return data

txt_dict = load_txt_data()


def load_kw_data():
    # try :
    path_file_ner = os.path.normpath(os.path.dirname(__file__) + os.sep + os.pardir)
    path_file_ner = os.path.join(path_file_ner, "Data-cache")
    path_file_ner = os.path.join(path_file_ner, "question_keywords.json")
    data = json.load(open(path_file_ner, encoding="utf-8"))
    return data


# except:
#     print("Error loading data")
#     return None




# except:
#     print("Error keyword loading data")
#     return None
def get_kw(file_addr):
    headers = {
        'accept': 'application/json',
    }
    files = {'document': open(file_addr,'rb')}
    response = requests.post('http://localhost:9000/concept/extract', headers=headers, files=files)
    kws = json.loads(response.text)['keywords']
    res = [i[0] for i in kws]
    return (res)



def kw_potential_candidates(curr_candid_ls, question, threshold_sc, verbose=0):
    VERBOSE = verbose
    
    # kw_1 = get_extracted_kw()
    curr_dir = os.path.dirname(__file__)
    target_dir = os.path.join(curr_dir, "Unsupervised-keyphrase-extraction", "src")
    # save the question in a text file
    save_txt_file = os.path.join(
        target_dir, "data", "Datasets", "EmJacc", "docsutf8", "1.txt"
    )
    text_file = open(save_txt_file, "w")
    text_file.write(question)
    text_file.close()

    kw_1 = " ".join(get_kw(save_txt_file))
    kw_dict = load_kw_data()
    curr_candid_scores = []

    for candidate in curr_candid_ls:
        score = keyword_score(
            kw_1.split(), kw_dict[candidate][0].split(), question, txt_dict[candidate]
        )
        if VERBOSE == 2:
            print("orig_ques -> ", question)
            print("kw_1 : ", kw_1)
            print()
            print("txt_dict[candidate]  -> ", txt_dict[candidate])
            print("kw_dict[candidate] : ", kw_dict[candidate][0])
            print()
            print("score : " + str(score))
            print()
            print("---------------------------------------")
        curr_candid_scores.append(score)

    final_candidates = []
    for ind, candidate in enumerate(curr_candid_ls):
        if curr_candid_scores[ind] > threshold_sc:
            final_candidates.append(candidate)

    if VERBOSE > 0:
        print(output_color.BLUE + "(KW) Potential_candidates : ")
        for id in final_candidates:
            print(id + " : " + txt_dict[id])
        print(output_color.END)

    return final_candidates


#
# Utils
#


def get_extracted_kw():
    curr_dir = os.path.dirname(__file__)
    xtr_txt_file = os.path.join(
        curr_dir,
        "Unsupervised-keyphrase-extraction",
        "src",
        "data",
        "Keywords",
        "EmbedRankSentenceBERT",
        "EmJacc",
        "1",
    )
    res = ""
    with open(xtr_txt_file) as f:
        Lines = f.readlines()
        for i in Lines:
            res += (" ".join(i.split()[:-1])) + " "
    os.remove(xtr_txt_file)
    return res


def intersection_list(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    List3 = list(set1.intersection(set2))
    return List3


def union_list(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    newList = list(set1.union(set2))
    return newList


def has_one_letter_diff(w1, w2):
    w1 = w1.lower()
    w2 = w2.lower()

    #   if(spelling.suggest(w1) == spelling.suggest(w2)):
    #     return True

    if abs(len(w1) - len(w2)) >= 2:
        return False

    amount = 0
    one = 0
    two = 0

    if len(w1) == len(w2):
        while one < len(w1):
            if w1[one] != w2[two]:
                amount += 1
            one += 1
            two += 1

        if amount == 1:
            return True
        else:
            return False
    else:
        if len(w2) > len(w1):
            temp = w1
            w1 = w2
            w2 = temp

        # w1 is 1 char longer than w2
        while two < len(w2):
            if w1[one] != w2[two]:
                if amount < 1:
                    amount += 1
                    if w2[two] != w1[one + 1]:
                        return False
                    else:
                        two -= 1
                else:
                    return False

            one += 1
            two += 1

    return True


def preprocess_keywords(keys):
    keys = keys.lower()
    ans = []
    doc = nlp(keys)
    keys = " ".join(
        [
            token.lemma_.strip("_")
            if len(token.lemma_) > 1 or (token.lemma_ in single_letter_elems)
            else ""
            for token in doc
        ]
    )
    sp = keys.split()

    for key in sp:
        ans.append(key)
    return ans


def keyword_score(keyword1, keyword2, question1, question2):
    diff = list(set(keyword1).difference(set(keyword2)))
    diff.extend(list(set(keyword2).difference(set(keyword1))))
    # block that ensures we handle cases where a keyword is detected by EmbedRank only in one question even though both the questions contain this keyword
    flag = True

    ques1_split = set(question1.split())
    ques2_split = set(question2.split())

    for word in diff:
        if not flag:
            break

        in_ques1 = False
        for ques1_word in ques1_split:
            if ques1_word == word or has_one_letter_diff(ques1_word, word):
                in_ques1 = True
                break

        in_ques2 = False
        for ques2_word in ques2_split:
            if ques2_word == word or has_one_letter_diff(ques2_word, word):
                in_ques2 = True
                break

        if not (in_ques1 and in_ques2):
            flag = False
            break

    if flag:
        return 1

    common_keyword = intersection_list(keyword1, keyword2)
    union_keyword = union_list(keyword1, keyword2)

    if union_keyword == []:  # suggestive model
        return 1

    return len(common_keyword) / len(union_keyword)
    # max(
    # len(common_keyword)/len(keyword1),
    # len(common_keyword)/len(keyword2)
    # )


# keyword_score("many π bond ferrocene", "many π ferrocene", "how many π bonds are present in ferrocene", "how many π are present in ferrocene"pip)
