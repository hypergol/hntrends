import hdbscan
from hypergol import Job
from hypergol import Task
from data_models.cluster_model import ClusterModel

class CreateClusterModels(Task):

    def __init__(self, *args, **kwargs):
        super(CreateClusterModels, self).__init__(*args, **kwargs)

    def get_jobs(self):
        nJobs = self.self.outputDataset.chunkCount
        return [Job(id_=k, total=nJobs) for k, in range(nJobs)]

    def source_iterator(self, parameters):
        yield (None, )

    def run(self, dummy, elements):
        dates = {element.date for date in elements}
        for k, date in enumerate(dates):
            if k % self.logAtEachN == 0:
                self.logger(f'models {k} / {len(dates)}')
            vectors = np.array([element.vector for element in elements if element.date==date])
            model = hdbscan.HDBSCAN()
            labels = model.fit_predict(vectors)
            self.output.append(ClusterModel(
                date=date,
                model=model,
                hids=[element.hid for element in elements if element.date==date],
                labels=labels
            ))
