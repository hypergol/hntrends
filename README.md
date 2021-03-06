# Hacker News Trends

The goal is to parse all stories and topics, extract entities and use them as labels in a doc2vec embedding.
Split the resulting embedding space by time and cluster with HDBSCAN each day.

Commands to create this project:

```
python -m hypergol.cli.create_project Hntrends
python -m hypergol.cli.create_data_model RawData title:str url:str text:str dead:int author:str score:int time:int timestamp:datetime htype:str hid:int:id parent:int descendants:int ranking:int deleted:int

python -m hypergol.cli.create_data_model Story title:str url:str author:str score:int time:int timestamp:datetime hid:int:id descendants:int ranking:int

python -m hypergol.cli.create_data_model Comment text:str author:str time:int timestamp:datetime hid:int:id parent:int
python -m hypergol.cli.create_data_model Document hid:int:id timestamp:datetime "tokens:List[str]" "labels:List[str]"

python3 -m hypergol.cli.create_task LoadData RawData --source
python3 -m hypergol.cli.create_task SelectStories RawData Story
python3 -m hypergol.cli.create_task SelectComments RawData Comment

python3 -m hypergol.cli.create_pipeline ProcessHackerNews LoadData SelectStories SelectComments RawData Comment Story


```

This project was generated with the Hypergol framework

Please see documentation for instructions: [https://hypergol.readthedocs.io/en/latest/](https://hypergol.readthedocs.io/en/latest/)

### Initialise git

Hypergol is heavily integrated with git, all projects must be in a git repository to ensure code and data lineage (to record which data was created by which version of the code).

Initialise git with:

```git init .```

Create the first commit (datasets record the last commit when they are created and without this there is nothing to record):

```git commit -m "First Commit!"```

The project now (and any time a file is changed but the change is not committed to the repo) is in a "dirty" stage. If you run a pipeline or train a model, the last commit will be recorded but that commit will not represent the code that is running! Add changes and commit:

```
git add .
git commit -m "All the files!"
```

If there are files that shouldn't be checked in ever to git they should be to the `.gitignore` file before `git add .`

Alternatively individual files can be added to git with `git add <filename>`.

### Make the virtual environment

Having dedicated virtual environment fully described by the projects `requirements.txt` is the recommended practice. Don't forget to `deactivate` the current virtual environment! Files from the environment are included in the projects `.gitignore` file and will ignored by git.

```
deactivate
./make_venv.sh
source .venv/bin/activate
```


### How to list existing Datasets (in Jupyter)

```
from hypergol import HypergolProject
project = HypergolProject(
    projectDirectory='<project_directory>/hntrends',
    dataDirectory=f'<data_directory>'
)
project.list_datasets(pattern='.*', asCode=True);
```

This will list all existing datasets that matches `pattern` as self contained executable code.


### How to start Tensorboard

It is recommended to start it in a screen session (`screen -S tensorboard`) so you can close the terminal window or if you disconnect from a remote Linux machine (reconnect with `screen -x tensorboard`). In the project directory:

```
screen -S tensorboard
source .venv/bin/activate
tensorboard --logdir=<data_directory>/hntrends/tensorboard/
```


### How to train your model

After implementing all components and required functions:

```
./train_hntrends.sh
```

This will execute the model manager's run() function with the prescribed schedule (training steps, evaluation steps, etc.). Training can be stopped with Ctrl-C, this will won't result in the corruption of the output dataset (datasets must be closed properly to generate their chk file after they are read only). This is possible because the entire training happen in a `try/finally` block.

### How to serve your model

In the generated `models/serve_hntrends.py` function specify the directory of the model to be served at:

```
MODEL_DIRECTORY = '<data_directory>/Hntrends/<branch>/models/hntrends/<epoch_number>'
```

then start serving with (port and host can be set in the shell script):

```
./serve_hntrends.sh
```


### How to call your model from python with requests

```
import requests
response = json.loads(requests.get('http://0.0.0.0:8000', headers={'accept': 'application/json'}).text)
modelLongName = response['model']
```

This allows to verify if indeed the intended model is served. The generated training script sets training day and the commit hash at that point to be part of the long name and to ensure that the exact conditions of training are available at serving. Long name should be used in logging to identify which model created an output. From v0.0.10 the long name is returned in the header of the response of `/output` endpoint as well in the `x-model-long-name` field.

To get the response of the model to a list of objects, see example below. Replace `ExampleOutput` with the correct output type and load a dataset into `ds`, use `list_datasets` from above to do this.

```
sys.path.insert(0, '<project_directory>/hntrends')
import requests
from itertools import islice

from data_models.example_output import ExampleOutput


with ds.open('r') as dsr:
    values = [value.to_data() for value in islice(dsr, 10)]


response = requests.post(
    'http://0.0.0.0:8000/output',
    headers={
        'accept': 'application/json',
        'Content-Type': 'application/json',
    },
    data=json.dumps(values)
)
outputs = [ExampleOutput.from_data(v) for v in json.loads(response.text)]
modelLongName = response.headers['x-model-long-name']
```

It is not recommended to do large scale evaluation through the API as the overhead per object is too high and it is single threaded.
