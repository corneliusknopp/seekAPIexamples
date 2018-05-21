
# coding: utf-8

# In[32]:


import requests
import json
import string
import getpass
import os
import fleep

# In[2]:


def remove_non_printable(text):
    return ''.join(i for i in text if i in string.printable)


# In[3]:


base_url = 'https://testing.sysmo-db.org'

headers = {"Content-type": "application/vnd.api+json",
           "Accept": "application/vnd.api+json",
           "Accept-Charset": "ISO-8859-1"}


# In[4]:


session = requests.Session()
session.headers.update(headers)
session.auth = (input('Username: '), getpass.getpass('Password: '))


# In[6]:


containing_project_id = 33

data_file = {}
data_file['data'] = {}
data_file['data']['type'] = 'data_files'
data_file['data']['attributes'] = {}
data_file['data']['attributes']['title'] = input('Please enter the name for the data_file: ')

local_filepath = os.path.abspath(input('Please enter the path to the local file: '))

local_file = open (local_filepath, mode='rb')
info = fleep.get(local_file.read(128))

mime_type = None
if info.mime:
  mime_type = info.mime[0]

local_blob = {'original_filename' : os.path.basename(local_filepath), 'content_type' : mime_type}

data_file['data']['attributes']['content_blobs'] = [local_blob]
data_file['data']['relationships'] = {}
data_file['data']['relationships']['projects'] = {}
data_file['data']['relationships']['projects']['data'] = [{'id' : containing_project_id, 'type' : 'projects'}]


# In[7]:


r = session.post(base_url + '/data_files', json=data_file)


# In[8]:


populated_data_file = r.json()


# In[9]:


data_file_id = populated_data_file['data']['id']
data_file_url = populated_data_file['data']['links']['self']


# In[13]:


blob_url = populated_data_file['data']['attributes']['content_blobs'][0]['link']


# In[35]:


# In[ ]:


local_file.seek(0)
upload = session.post(blob_url, data=local_file.read())
