import os
import fire
from hypergol import HypergolProject
from hypergol.hypergol_project import RepoManager
from hypergol import Pipeline
from tasks.load_data import LoadData
from tasks.clean_text import CleanText
from tasks.process_with_spacy import ProcessWithSpacy
from data_models.raw_data import RawData


def process_hacker_news(filePattern, dataDirectory, threads=1, raiseIfDirty=True, force=False): 
    project = HypergolProject(
        dataDirectory=dataDirectory, 
        force=force,
        repoManager=RepoManager(repoDirectory=os.getcwd(), raiseIfDirty=raiseIfDirty)
    )
    rawData = project.datasetFactory.get(dataType=RawData, name='raw_data', chunkCount=256)
    loadData = LoadData(
        logAtEachN=200_000
        filePattern=filePattern,
        outputDataset=rawData
    )

    # cleanText = CleanText(
    #     inputDatasets=[rawData],
    #     outputDataset=textData,
    # )
    # processWithSpacy = ProcessWithSpacy(
    #     inputDatasets=[exampleInputDataset1,  exampleInputDataset2],
    #     outputDataset=exampleOutputDataset,
    # )

    pipeline = Pipeline(
        tasks=[
            loadData,
            # cleanText,
            # processWithSpacy,
        ]
    )
    pipeline.run(threads=threads)


if __name__ == '__main__':
    fire.Fire(process_hacker_news)
