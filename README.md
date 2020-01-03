# MT2IR

Typically, preparing the system involves the following:

1. Install the software dependencies
1. Install elasticsearch and trec_eval
1. Start elasticsearch
1. Run experiments
1. Stop elasticsearch

## Dependencies
* Python 3.7
* [NumPy](http://www.numpy.org/), tested with 1.15.4
* [Python Elastic Search Client](https://elasticsearch-py.readthedocs.io/en/master/), `pip install elasticsearch`
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), use to parse sgml files (`pip install bs4`)
* [jenkspy 0.1.5](https://github.com/mthh/jenkspy), a fast python implementation of jenks natural breaks algorithm

## Usage
| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

## Installation
* Install python dependencies  `pip install -r requirements.txt`
* Install external tools (elasticsearch and trec_eval) `bash scripts/install_external_tools.sh`

## Start and Stop ElasticSearch
`./scripts/server.sh [start | stop]`

## Run evaluation
python evaluate.py sample/en-de.ref.sgm sample/en-de.mt.sgm
