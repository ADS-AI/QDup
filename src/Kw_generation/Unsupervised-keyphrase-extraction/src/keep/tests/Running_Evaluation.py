import os
from keep import SIGTREC_Eval
from keep import Rake
from keep import YAKE
from keep import MultiPartiteRank
from keep import TopicalPageRank
from keep import TopicRank
from keep import PositionRank
from keep import SingleRank
from keep import TextRank
from keep import KPMiner
from keep import TFIDF
from keep import KEA

# Some algorithms have a normalization parameter which may be defined with None, stemming or lemmatization
normalization = None  # Other options: "stemming" (porter) and "lemmatization"

# Num of Keyphrases to Retrieve
numOfKeyphrases = 20

# Num of folds for training KEA
nFolds = 5

"""
ListOfDatasets = ['500N-KPCrowd-v1.1', '110-PT-BN-KP', 'KWTweets', 'cacic', 'citeulike180',
                  'fao30', 'fao780', 'Inspec', 'kdd', 'Krapivin2009',
                  'Nguyen2007', 'pak2018', 'PubMed', 'Schutz2008', 'SemEval2010',
                  'SemEval2017', 'theses100', 'wicc', 'wiki20', 'WikiNews', 'www']
"""
ListOfDatasets = ["500N-KPCrowd-v1.1"]

# ListOfAlgorithms = ['RAKE', 'YAKE', 'MultiPartiteRank', 'TopicalPageRank', 'TopicRank', 'SingleRank', 'TextRank', 'KPMiner', 'TFIDF', 'KEA']
ListOfAlgorithms = ["YAKE", "RAKE"]

# Please replace the following path by your own path, where data is the folder where the datasets may be found.
pathData = (
    "H:/Backup/Research/Programming/JupyterNotebooks/Python/KeywordExtractors/data"
)
pathOutput = pathData + "/conversor/output/"
pathDataset = pathData + "/Datasets/"
pathKeyphrases = pathData + "/Keywords/"

EvaluationStemming = False

statistical_test = ["student"]  # wilcoxon

measures = ["map", "P.5"]

formatOutput = "df"  # options: 'csv', 'html', 'json', 'latex', 'sql', 'string', 'df'

for algorithm in ListOfAlgorithms:
    print("\n")
    print(
        "----------------------------------------------------------------------------------------"
    )
    print(f"Prepare Evaluation for \033[1m{algorithm}\033[0m algorithm")

    for i in range(len(ListOfDatasets)):
        dataset_name = ListOfDatasets[i]
        print("\n----------------------------------")
        print(f" dataset_name = {dataset_name}")
        print("----------------------------------")

        if algorithm == "RAKE":
            Rake_object = Rake(numOfKeyphrases, pathData, dataset_name)
            Rake_object.ExtractKeyphrases()
            Rake_object.Convert2Trec_Eval(EvaluationStemming)
        elif algorithm == "YAKE":
            YAKE_object = YAKE(numOfKeyphrases, pathData, dataset_name)
            YAKE_object.ExtractKeyphrases()
            YAKE_object.Convert2Trec_Eval(EvaluationStemming)
        elif algorithm == "MultiPartiteRank":
            MultiPartiteRank_object = MultiPartiteRank(
                numOfKeyphrases, pathData, dataset_name
            )
            MultiPartiteRank_object.ExtractKeyphrases()
            MultiPartiteRank_object.Convert2Trec_Eval(EvaluationStemming)
        elif algorithm == "TopicalPageRank":
            TopicalPageRank_object = TopicalPageRank(
                numOfKeyphrases, pathData, dataset_name, normalization
            )
            TopicalPageRank_object.ExtractKeyphrases()
            TopicalPageRank_object.Convert2Trec_Eval(EvaluationStemming)
        elif algorithm == "TopicRank":
            TopicRank_object = TopicRank(numOfKeyphrases, pathData, dataset_name)
            TopicRank_object.ExtractKeyphrases()
            TopicRank_object.Convert2Trec_Eval(EvaluationStemming)
        elif algorithm == "PositionRank":
            PositionRank_object = PositionRank(
                numOfKeyphrases, pathData, dataset_name, normalization
            )
            PositionRank_object.ExtractKeyphrases()
            PositionRank_object.Convert2Trec_Eval(EvaluationStemming)
        elif algorithm == "SingleRank":
            SingleRank_object = SingleRank(
                numOfKeyphrases, pathData, dataset_name, normalization
            )
            SingleRank_object.ExtractKeyphrases()
            SingleRank_object.Convert2Trec_Eval(EvaluationStemming)
        elif algorithm == "TextRank":
            TextRank_object = TextRank(
                numOfKeyphrases, pathData, dataset_name, normalization
            )
            TextRank_object.ExtractKeyphrases()
            TextRank_object.Convert2Trec_Eval(EvaluationStemming)
        elif algorithm == "KPMiner":
            KPMiner_object = KPMiner(
                numOfKeyphrases, pathData, dataset_name, normalization
            )
            KPMiner_object.ExtractKeyphrases()
            KPMiner_object.Convert2Trec_Eval(EvaluationStemming)
        elif algorithm == "TFIDF":
            TFIDF_object = TFIDF(numOfKeyphrases, pathData, dataset_name, normalization)
            TFIDF_object.ExtractKeyphrases()
            TFIDF_object.Convert2Trec_Eval(EvaluationStemming)
        elif algorithm == "KEA":
            KEA_object = KEA(numOfKeyphrases, pathData, dataset_name, normalization)
            KEA_object.ExtractKeyphrases(nFolds)
            KEA_object.Convert2Trec_Eval(EvaluationStemming)

# Run Evaluate
for dataset in ListOfDatasets:
    print("\n")
    print(
        "----------------------------------------------------------------------------------------"
    )
    print(f"Running Evaluation for \033[1m{dataset}\033[0m dataset")

    path2qrel_file = f"{pathOutput}{dataset}.qrel"
    datasetid = os.path.basename(path2qrel_file)

    resultsFiles = []
    for alg in ListOfAlgorithms:
        resultsFiles.append(f"{pathOutput}{dataset}_{alg}.out")

    sig = SIGTREC_Eval()
    results = sig.Evaluate(
        path2qrel_file,
        datasetid,
        resultsFiles,
        measures,
        statistical_test,
        formatOutput,
    )

    for res in results:
        print(res)
