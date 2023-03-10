import os
import string
from sklearn.model_selection import KFold
from nltk.stem.snowball import SnowballStemmer
from glob import glob
import numpy as np
from shutil import copyfile
from pke import compute_document_frequency
from pke import compute_lda_model
import pke
from keep.conversor.convert2trec import Convert

ISO_to_language_stemming_SnowballStemmer = {
    "en": "english",
    "pt": "portuguese",
    "fr": "french",
    "es": "spanish",
    "it": "italian",
    "nl": "dutch",
    "de": "german",
    "da": "danish",
    "fi": "finnish",
    "da": "danish",
    "hu": "hungarian",
    "nb": "norwegian",
    "ro": "romanian",
    "ru": "russian",
    "sv": "swedish",
}


def getlanguage(pathDataset):
    with open(pathDataset + "/lan.txt", encoding="utf8") as fil:
        lan = fil.read()
    return lan[:2]


def Convert2TrecEval(
    pathToDatasetName,
    EvaluationStemming,
    outputPath,
    keywordsPath,
    dataset_name,
    algorithmName,
):
    print("\nConvert to trec_eval format")
    conv = Convert(pathToDatasetName, EvaluationStemming)

    # Create out file
    conv.CreateOutFile(outputPath, keywordsPath, dataset_name, algorithmName)

    # Creat qrels file
    conv.CreateQrelFile(outputPath, dataset_name)


def CreateKeywordsFolder(keywordsPath):
    # Set the folder where keywords are going to be saved
    print(f"Keyphrases will be saved in this folder: {keywordsPath}\n")

    if not os.path.exists(keywordsPath):
        print(f"Output Keyphrases Folder doesn't exit: {keywordsPath}. Let's Create it")
        os.makedirs(keywordsPath)
    else:
        print(f"Output Keyphrases Folder already exists.")


def LoadFiles(pathToCollectionOfDocs):
    # Gets all files within the specified folder
    listFile = glob(pathToCollectionOfDocs)
    return listFile


def load_stop_words(lan):
    """
    Utility function to load stop words from a file and return as a list of words
    @param stop_word_file Path and file name of a file containing stop words.
    @return list A list of stop words.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))

    local_path = os.path.join(
        "/StopwordsList/", "stopwords_" + lan[:2].lower() + ".txt"
    )
    resource_path = dir_path + local_path
    with open(resource_path, encoding="utf8") as fil:
        stopwords_ = fil.readlines()
        stopwords_ = [s[:-1] for s in stopwords_]
    return set(stopwords_)


def ComputeDF(pathToCollectionOfDocs, lang, normalization, pathToDFFile):
    """Compute Document Frequency (DF) counts from a collection of documents.

    N-grams up to 3-grams are extracted and converted to their n-stems forms.
    Those containing a token that occurs in a stoplist are filtered out.
    Output file is in compressed (gzip) tab-separated-values format (tsv.gz).
    """

    # path to the collection of documents
    print(
        f"DF will be computed on top of the following collection of docs: {pathToCollectionOfDocs}"
    )

    if os.path.exists(pathToDFFile):
        print(f"DF Model already exists here:  {pathToDFFile} ")
    else:
        print(
            f"DF Model doesn't exist. It will be created (and may take a while) and will be saved here: {pathToDFFile}"
        )
        stoplist = list(string.punctuation)
        stoplist += ["-lrb-", "-rrb-", "-lcb-", "-rcb-", "-lsb-", "-rsb-"]
        stoplist += load_stop_words(lang)

        compute_document_frequency(
            pathToCollectionOfDocs,
            pathToDFFile,
            extension="txt",
            language=lang,
            normalization=normalization,
            stoplist=stoplist,
        )
    # model end


def CreateLatentDirichletAllocationModel(
    pathDataset, dataset_name, lang, normalization, pathToLDAFolder
):
    print("I am going to check if LDA model exists. If it doesn't I will create it.")

    # path to the collection of documents
    pathToCollectionOfDocs = pathDataset + "/docsutf8"
    print(f"\nPath to the collection of docs = {pathToCollectionOfDocs}")

    # model init
    pathToLDAFile = pathToLDAFolder + dataset_name + "_lda.gz"
    print(f"Path to LDA file = {pathToLDAFile}")

    if os.path.exists(pathToLDAFile):
        print(f"Model =  {pathToLDAFile} already exists")
    else:
        print(
            "Model doesn't exist. Let's create a new model based on the collection of documents. It may take a while"
        )
        # Test if lan exists in spacy models. If not considers model en
        if lang not in ["en", "es", "pt", "fr", "it", "nl", "de"]:
            compute_lda_model(
                pathToCollectionOfDocs,
                pathToLDAFile,
                n_topics=500,
                extension="txt",
                language="en",
                normalization=normalization,
            )
        else:
            compute_lda_model(
                pathToCollectionOfDocs,
                pathToLDAFile,
                n_topics=500,
                extension="txt",
                language=lang,
                normalization=normalization,
            )
        print("Model just created")
    # model end


def get_goldKeywords(filename, stem=None):
    result = []
    with open(filename, encoding="utf8") as filin:
        if stem == None:
            for kw in filin.readlines():
                kw = kw.lower().split()
                result.append(" ".join([word for word in kw]))
        else:
            for kw in filin.readlines():
                kw = kw.lower().split()
                result.append(" ".join([stem.stem(word) for word in kw]))
    return result


def save_goldKeywords(gkw_filename, gold_ann):
    if not os.path.exists(os.path.dirname(gkw_filename)):
        os.makedirs(os.path.dirname(gkw_filename))

    with open(gkw_filename, "w", encoding="utf8") as filout:
        for kw in gold_ann:
            filout.write(kw + "\n")


def SplitDatasetIntoFolds(pathDataset, docs_path, nFolds):
    kf = KFold(n_splits=nFolds)

    """
    In a dataset of 100 docs, train_index gives for the 1st fold the indexes [0,..,79], while test_index give the indexes [80, 99]
    As docs_path is an array of the dataset text paths, getting the training documents path is as simple as docs_path[train_index]
    """
    for i, (train_index, test_index) in enumerate(kf.split(docs_path), 1):
        fold_path = pathDataset + "/folds/fold" + str(i)
        if not os.path.exists(fold_path + "/train"):
            print(f"Fold {i} don't exist. Let's create it")
            os.makedirs(fold_path + "/train")
            os.makedirs(fold_path + "/test")

            """
            Copies each of the files existing in the array of train_docs of fold i to the folder of folds
            For instance for a dataset of 100 docs, and considering i = 1 (1st fold) it copies the 1st 80 docs of tranning docs
            into the folder DatasetName\folds\fold1\train\
            """
            # Get the path of the training docs for fold i
            train_docs = docs_path[train_index]
            for doc_path in train_docs:
                docname = os.path.basename(doc_path)
                copyfile(doc_path, fold_path + "/train/" + docname)

            """
            Copies each of the files existing in the array of testing_docs of fold i to the folder of folds
            For instance for a dataset of 100 docs, and considering i = 0 (1st fold) it copies the last 20 docs of testing docs
            into the folder DatasetName\folds\fold1\test\
            """
            # Get the path of the testing docs for fold i
            test_docs = docs_path[test_index]
            for doc_path in test_docs:
                docname = os.path.basename(doc_path)
                copyfile(doc_path, fold_path + "/test/" + docname)
        else:
            print(f"Fold {i} already exits")


def CreateGroundTruthFile(pathToDatasetName, normalization, lang):

    groundTruthFile = pathToDatasetName + "/gold-annotation.txt"

    # Create the Ground-TruthFile
    if os.path.exists(groundTruthFile):
        print(
            f"STEP 1: Ground-Truth file =  {pathToDatasetName}/gold-annotation.txt already exists"
        )
    else:
        print(
            f"STEP 1: Ground-Truth file doesn't exists. Let's create it here: {pathToDatasetName}/gold-annotation.txt"
        )

        # docs_path keeps the path of all the txt files found within the collection of documents (within the folder /docsutf8)
        docs_path = np.array(glob(pathToDatasetName + "/docsutf8/" + "*.txt"))

        if normalization == "stemming":
            if lang == "en":
                # create a new instance of a porter stemmer
                stemmer = SnowballStemmer("porter")
            else:
                # create a new instance of a porter stemmer
                stemmer = SnowballStemmer(
                    ISO_to_language_stemming_SnowballStemmer[lang],
                    ignore_stopwords=True,
                )
        else:
            stemmer = None

        gold_annotation = []

        for doc_path in docs_path:
            docname = os.path.basename(
                doc_path
            )  # keeps the basename of the file (e.g., art_and_culture-20880868.txt)

            # Create the ground-truth file
            docname = ".".join(os.path.basename(docname).split(".")[0:-1])
            key_path = pathToDatasetName + "/keys/" + docname + ".key"

            kws = get_goldKeywords(
                key_path, stemmer
            )  # (e.g., art_and_culture-20880868.key)
            gold_annotation.append(f"{docname} : {','.join(kws)}")

        save_goldKeywords(groundTruthFile, gold_annotation)

        print("Created!")

    return groundTruthFile


def CrossValidation(pathToDatasetName, nFolds):
    # Cross-Validation Evaluation Step

    print("\nCreating folds for the evaluation step")
    # docs_path keeps the path of all the txt files found within the collection of documents (within the folder /docsutf8)
    docs_path = np.array(glob(pathToDatasetName + "/docsutf8/" + "*.txt"))

    SplitDatasetIntoFolds(pathToDatasetName, docs_path, nFolds)
