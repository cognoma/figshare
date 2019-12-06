# figshare

This is a simple client for the figshare API in python. Currently the
following actions are implemented

* create_article
* update_article
* get_article_details
* list_files
* get_file_details
* retrieve_files_from_article

## Install

```shell
git clone https://github.com/cognoma/figshare.git
python setup.py install
```

For development, I recommend:

```shell
python setup.py develop
```

## Execution

To use this Python module, here's a demonstration of initiating the API and
retrieving information from Figshare API. This was done using
[iPython](https://ipython.readthedocs.io/en/stable/), but
other Python-based methods will work as well:

```python
from figshare.figshare import Figshare
fs = Figshare()
article_id = 4757131
fs.get_article_details(article_id)
```

That will produce a dictionary object.  Here's a snippet of the first and last few lines:

```json
{'defined_type_name': 'dataset',
'embargo_date': None,
'citation': 'Lake, Sean; Wright, Edward L.; Assef, Roberto J.; Jarrett, Thomas H.; Petty, Sara; Stanford, Spencer A.; et al. (2019): Evolving Extragalactic Background and Luminosity Density. figshare. Dataset. https://doi.org/10.6084/m9.figshare.4757131.v1',
'url_private_api': 'https://api.figshare.com/v2/account/articles/4757131',
'status': 'public',
'created_date': '2019-08-07T07:54:50Z',
'group_id': None,
'is_metadata_record': False,
'modified_date': '2019-08-07T07:54:51Z'}
```

## Dependencies

The following python libraries need to be installed

* requests

