import os
import pke
import string
from keep.utility import (
    load_stop_words,
    CreateGroundTruthFile,
    CrossValidation,
    getlanguage,
    CreateKeywordsFolder,
    LoadFiles,
    ComputeDF,
    Convert2TrecEval,
)


class KEA(object):
    def __init__(self, numOfKeywords, pathData, dataset_name, normalization):
        self.__lan = getlanguage(pathData + "/Datasets/" + dataset_name)
        self.__numOfKeywords = numOfKeywords
        self.__dataset_name = dataset_name
        self.__normalization = normalization
        self.__pathData = pathData
        self.__pathToKeaModelsFolder = ""
        self.__pathToKEAFile = ""
        self.__pathToDFFile = ""
        self.__pathToCollectionOfDocs = ""
        self.__pathToDatasetName = self.__pathData + "/Datasets/" + self.__dataset_name
        self.__algorithmName = "KEA"
        self.__keywordsPath = self.__pathData + "/Keywords/KEA/" + self.__dataset_name
        self.__outputPath = self.__pathData + "/conversor/output/"

    def LoadDatasetFiles(self, docsFolder="/docsutf8/*"):
        # Gets all files within the dataset fold.
        # When no docsFolder is specified, the system will load the entire set of documents, which can be find under the docsutf8 folder
        # While this is the default behavior, this method is prepared to read the files from a specified folder (this will usually be the case when
        # we are conducting evaluation, in which case, we should be reading docs from the training document of a given fold
        listFile = LoadFiles(self.__pathToDatasetName + docsFolder)
        print(
            f"\ndatasetID = {self.__dataset_name}; Number of Files = {len(listFile)}; Language of the Dataset = {self.__lan}"
        )
        return listFile

    def CreateKeywordsOutputFolder(self):
        # Set the folder where keywords are going to be saved
        CreateKeywordsFolder(self.__keywordsPath)

    def runSingleDoc(self, doc):
        # Get keywords for a single doc. It will only retrieve the keywords for further processing
        # Either they will be printed in case we really just want to extract keywords from a single doc
        # Or they will be saved in case we are extracting keywords from multiple docs (that is, if this method is called externally by runMultipleDocs)
        # 1. create extractor.
        extractor = pke.supervised.Kea()

        # 2. load the content of the document in a given language
        extractor.load_document(
            input=doc, language=self.__lan, normalization=self.__normalization
        )

        # 3. select 1-3 grams that do not start or end with a stopword as
        #    candidates. Candidates that contain punctuation marks as words
        #    are discarded.
        stoplist = list(string.punctuation)
        stoplist += ["-lrb-", "-rrb-", "-lcb-", "-rcb-", "-lsb-", "-rsb-"]
        a = load_stop_words(self.__lan)
        stoplist += load_stop_words(self.__lan)
        extractor.candidate_selection(stoplist=stoplist)

        try:
            # 4. classify candidates as keyphrase or not keyphrase.
            # df = pke.load_document_frequency_file(input_file= self.__pathToDFFile +  "/df.tsv.gz")
            df = pke.load_document_frequency_file(input_file=self.__pathToDFFile)
            # extractor.candidate_weighting(model_file=self.__pathToKeaModelsFolder + "/model.pickle", df=df)
            extractor.candidate_weighting(model_file=self.__pathToKEAFile, df=df)

            # 5. get the numOfKeywords-highest scored candidates as keyphrases
            keywords = extractor.get_n_best(n=self.__numOfKeywords)
        except:
            keywords = []

        return keywords

    def runMultipleDocs(self, listOfDocs):
        self.CreateKeywordsOutputFolder()

        for j, doc in enumerate(listOfDocs):
            # docID keeps the name of the file (without the extension)
            docID = ".".join(os.path.basename(doc).split(".")[0:-1])

            keywords = self.runSingleDoc(doc)

            # Save the keywords; score (on Algorithms/NameOfAlg/Keywords/NameOfDataset
            with open(
                os.path.join(self.__keywordsPath, docID), "w", encoding="utf-8"
            ) as out:
                for (key, score) in keywords:
                    out.write(f"{key} {score}\n")

            # Track the status of the task
            print(f"\rFile: {j+1}/{len(listOfDocs)}", end="")

        print(f"\n100% of the Extraction Concluded")

    def TrainingModel(self, nFolds=1):
        # Check if the ground-truth file exists under the data/Datasets/NameOfDataset/folds. If it doesn't: create it as it will be used to train the KEA algorithm
        groundTruthFile = CreateGroundTruthFile(
            self.__pathToDatasetName, self.__normalization, self.__lan
        )

        # Training the Model
        if (
            nFolds == 1
        ):  # It means that it should create a model under the entire dataset. The purpose here is jsut to extract keywords (without having in mind any kind of evaluation)
            self.__pathToCollectionOfDocs = (
                self.__pathData + "/Datasets/" + self.__dataset_name + "/docsutf8"
            )
            self.__pathToDFFile = (
                self.__pathData
                + "/Models/Supervised/dfs/"
                + self.__dataset_name
                + "/df.tsv.gz"
            )
            self.__pathToKEAFile = (
                self.__pathData
                + "/Models/Supervised/"
                + self.__algorithmName
                + "/"
                + self.__dataset_name
                + "/model.pickle"
            )
            self.__pathToKeaModelsFolder = (
                self.__pathData
                + "/Models/Supervised/"
                + self.__algorithmName
                + "/"
                + self.__dataset_name
            )

            self.TrainingKEAModel(
                self.__pathToCollectionOfDocs,
                groundTruthFile,
                self.__lan,
                self.__normalization,
                self.__pathToDFFile,
                self.__pathToKEAFile,
                self.__pathToKeaModelsFolder,
            )
            # Track the status of the task
            print(f"KEA Model created", end="")
        else:  # Used for evaluation purposes. That is, it will create one model per each fold - used together with cross-validation
            for f in range(1, nFolds + 1):
                self.__pathToCollectionOfDocs = (
                    self.__pathData
                    + "/Datasets/"
                    + self.__dataset_name
                    + "/folds/fold"
                    + str(f)
                    + "/train"
                )
                self.__pathToDFFile = (
                    self.__pathData
                    + "/Models/Supervised/dfs/"
                    + self.__dataset_name
                    + "/folds"
                    + "/fold"
                    + str(f)
                    + "/df.tsv.gz"
                )
                self.__pathToKEAFile = (
                    self.__pathData
                    + "/Models/Supervised/"
                    + self.__algorithmName
                    + "/"
                    + self.__dataset_name
                    + "/folds"
                    + "/fold"
                    + str(f)
                    + "/model.pickle"
                )
                self.__pathToKeaModelsFolder = (
                    self.__pathData
                    + "/Models/Supervised/"
                    + self.__algorithmName
                    + "/"
                    + self.__dataset_name
                    + "/folds"
                    + "/fold"
                    + str(f)
                )

                # Track the status of the task
                print(f"\n--> Processing fold {f}/{nFolds}", end="")

                self.TrainingKEAModel(
                    self.__pathToCollectionOfDocs,
                    groundTruthFile,
                    self.__lan,
                    self.__normalization,
                    self.__pathToDFFile,
                    self.__pathToKEAFile,
                    self.__pathToKeaModelsFolder,
                )

    # Method that enables to proceed with the Evaluation stage

    def TrainingKEAModel(
        self,
        pathToCollectionOfDocs,
        groundTruthFile,
        lang,
        normalization,
        pathToDFFile,
        pathToKEAFile,
        pathToKeaModelsFolder,
    ):
        print(f"\nSTEP 2: Compute Document Frequency")
        ComputeDF(pathToCollectionOfDocs, lang, normalization, pathToDFFile)
        df = pke.load_document_frequency_file(input_file=pathToDFFile)

        print(
            f"\nSTEP 3: Train KEA Model on top of the following set of docs: {pathToCollectionOfDocs}"
        )

        if os.path.exists(pathToKEAFile):
            print(f"KEA Model File already exists here:  {pathToKEAFile} ")
        else:
            print(
                f"KEA Model doesn't exists. Let's create here: {pathToCollectionOfDocs}. It may take a while."
            )
            # If folder Models does not exist: Create it
            if not os.path.exists(pathToKeaModelsFolder):
                os.makedirs(pathToKeaModelsFolder)

            pke.train_supervised_model(
                input_dir=pathToCollectionOfDocs,
                reference_file=groundTruthFile,
                model_file=pathToKEAFile,
                extension="txt",
                language=lang,
                normalization=normalization,
                df=df,
                model=pke.supervised.Kea(),
            )

    # Evaluation
    def ExtractKeyphrases(self, nFolds):
        # Split the dataset into folds
        print(
            f"\n------------------------------Cross-Validation Process--------------------------"
        )
        CrossValidation(self.__pathToDatasetName, nFolds)

        # Train the model, that is, create a KEA model (model.pickle) and a DF model (df.tsv.gz) for each of the nFolds (based on the training documents)
        print(
            f"\n------------------------------{self.__algorithmName} Training-Model Process--------------------------"
        )
        self.TrainingModel(nFolds)

        # Gets keyphrases for each of the 5 testing folds, based on the KEA MODEL obtained from the training documents of the corresponding fold
        for f in range(1, nFolds + 1):
            print(
                f"\n\n-----------------Extract Keyphrases from the docs of Test folder belonging to fold-{f}--------------------------"
            )
            listOfDocs = self.LoadDatasetFiles(f"/folds/fold{f}/test/*")

            self.runMultipleDocs(listOfDocs)

    def Convert2Trec_Eval(self, EvaluationStemming=False):
        Convert2TrecEval(
            self.__pathToDatasetName,
            EvaluationStemming,
            self.__outputPath,
            self.__keywordsPath,
            self.__dataset_name,
            self.__algorithmName,
        )
