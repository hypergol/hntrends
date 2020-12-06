from hypergol import Task
from data_models.raw_data import RawData
from data_models.story import Story


class SelectStories(Task):

    def __init__(self, exampleParameter, *args, **kwargs):
        super(SelectStories, self).__init__(*args, **kwargs)
        # TODO: all member variables must be pickle-able, otherwise use the "Delayed" methodology
        # TODO: (e.g. for a DB connection), see the documentation <add link here>
        self.exampleParameter = exampleParameter

    def init(self):
        # TODO: initialise members that are NOT "Delayed" here (e.g. load spacy model)
        pass

    def run(self, exampleInputObject1, exampleInputObject2):
        raise NotImplementedError(f'{self.__class__.__name__} must implement run()')
        self.output.append(exampleOutputObject)
