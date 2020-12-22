from hypergol import Job
from hypergol import Task
from data_models.element import Element


class CreateClusterModels(Task):

    def __init__(self, exampleParameter, *args, **kwargs):
        super(CreateClusterModels, self).__init__(*args, **kwargs)
        # TODO: all member variables must be pickle-able, otherwise use the "Delayed" methodology
        # TODO: (e.g. for a DB connection), see the documentation <add link here>
        self.exampleParameter = exampleParameter

    def init(self):
        # TODO: initialise members that are NOT "Delayed" here (e.g. load spacy model)
        pass

    def get_jobs(self):
        raise NotImplementedError(f'{self.__class__.__name__} must implement get_jobs()')
        # TODO: Return a list of Job classes here that will be passed on to the source_iterator
        return [Job(id_=k, total= ..., parameters={...}) for k, ... in enumerate(...)]

    def source_iterator(self, parameters):
        raise NotImplementedError(f'{self.__class__.__name__} must implement source_iterator()')
        # TODO: use the parameters (from Job) to open
        # TODO: use yield in this function instead of return while you are consuming your source data
        # TODO: return type must be list or tuple as the * operator will be used on it
        yield (exampleData, )

    def run(self, exampleData):
        raise NotImplementedError(f'{self.__class__.__name__} must implement run()')
        # TODO: Use the exampleData from source_iterator to construct a domain object
        self.output.append(exampleOutputObject)
