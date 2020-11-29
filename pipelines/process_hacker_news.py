import fire
from hypergol import HypergolProject
from hypergol import Pipeline
from tasks.load_data import LoadData
from tasks.clean_text import CleanText
from tasks.process_with_spacy import ProcessWithSpacy
from data_models.raw_data import RawData


def process_hacker_news(filePattern, threads=1, force=False):
    project = HypergolProject(dataDirectory='.', force=force)
    rawDatas = project.datasetFactory.get(dataType=RawData, name='raw_datas')
    loadData = LoadData(
        filePattern=filePattern
        outputDataset=rawData,
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
