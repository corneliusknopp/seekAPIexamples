# -*- coding: utf-8 -*-

"""create_remote_data_file.ipynb

Import the libraries so that they can be used within the notebook

* **requests** is used to make HTTP calls
* **json** is used to encode and decode strings into JSON
* **string** is used to perform text manipulation and checking
* **getpass** is used to do non-echoing password input
* **fleep** is used to determine the mime type of files
"""

import requests
import json
import string
import getpass
import os
import fleep

"""The **base_url** holds the URL to the SEEK instance that will be used in the notebook

**headers** holds the HTTP headers that will be sent with every HTTP call

* **Content-type: application/vnd.api+json** - indicates that any data sent will be in JSON API format
* **Accept: application/vnd.api+json** - indicates that the notebook expects any data returned to be in JSON API format
* **Accept-Charset: ISO-8859-1** - indicates that the notebook expects any text returned to be in ISO-8859-1 character set
"""

base_url = 'https://testing.sysmo-db.org'

headers = {"Content-type": "application/vnd.api+json",
           "Accept": "application/vnd.api+json",
           "Accept-Charset": "ISO-8859-1"}


"""Create a **requests** HTTP **Session**. A **Session** has re-usable settings such as **headers**

The **authorization** is username and password. The user is prompted for this information.
"""

session = requests.Session()
session.headers.update(headers)
session.auth = (input('Username: '), getpass.getpass('Password: '))

"""The **data_file** will be created within **Project** 33"""

containing_project_id = 33

"""Initialize a **data_file** as a hierarchical structure

The title of the **data_file** is input by the user

The **data_file** is linked to the containing **project**
"""

data_file = {}
data_file['data'] = {}
data_file['data']['type'] = 'data_files'
data_file['data']['attributes'] = {}
data_file['data']['attributes']['title'] = input('Please enter the name for the data_file: ')

"""Read the filepath to the local file and determine its mime_type"""
local_filepath = os.path.abspath(input('Please enter the path to the local file: '))

local_file = open (local_filepath, mode='rb')
info = fleep.get(local_file.read(128))

mime_type = None
if info.mime:
  mime_type = info.mime[0]

"""Create a placeholder for the local data"""

local_blob = {'original_filename' : os.path.basename(local_filepath), 'content_type' : mime_type}

"""Update the **data_file** with the placeholder"""

data_file['data']['attributes']['content_blobs'] = [local_blob]
data_file['data']['relationships'] = {}
data_file['data']['relationships']['projects'] = {}
data_file['data']['relationships']['projects']['data'] = [{'id' : containing_project_id, 'type' : 'projects'}]


"""**POST** the **data_file** to the SEEK instance

Check the status of the response
"""

r = session.post(base_url + '/data_files', json=data_file)
r.raise_for_status()

"""Extract the created **data_file** from JSON into **populated_data_file**"""

populated_data_file = r.json()

"""Extract the id and URL to the newly created **data_file**"""

data_file_id = populated_data_file['data']['id']
data_file_url = populated_data_file['data']['links']['self']

"""Extract the URL for the local data"""

blob_url = populated_data_file['data']['attributes']['content_blobs'][0]['link']

"""Reset the local file and upload it to the URL"""

local_file.seek(0)
upload = session.put(blob_url, data=local_file.read(), headers={'Content-Type': 'application/octet-stream'})
upload.raise_for_status()
