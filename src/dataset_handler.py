import os
import requests
import pprint
import json

# Logging
import logging
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
handler_format = logging.Formatter('%(asctime)s : [%(name)s - %(lineno)d] %(levelname)-8s - %(message)s')
stream_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)

class Datasethandler:
  def __init__(self):
    self.id = 'admin'
    self.password = 'password'
    self.project_id = '631a6a99-0b30-425a-bdf2-af4532ff9451'
    self.host_url = 'http://localhost:8000'

  def get_datasets(self):
    response = requests.get(
      '%s/api/datarepository/datasets/' % (self.host_url),
      auth=(self.id, self.password),
    )
    pprint.pprint(response.json())

  def get_dataset(self, dataset_uuid: str):
    response = requests.get(
      '%s/api/datarepository/datasets/%s/' % (self.host_url, dataset_uuid),
      auth=(self.id, self.password)
    )
    pprint.pprint(response.json())

  def search_dataset(self, name: str, datatype_name: str):
    data = {'name': name, 'datatype_name': datatype_name}
    response = requests.post(
      '%s/api/datarepository/datasets/search/' % (self.host_url),
      auth=(self.id, self.password),
      data=json.dumps(data)
    )
    pprint.pprint(response.text)

  def create_dataset(self, name: str, datatype_uuid: str):
    data = {'name': name, 'project': self.project_id, 'datatype': datatype_uuid}
    response = requests.post(
      '%s/api/datarepository/datasets/' % (self.host_url),
      headers={'Content-Type': 'application/json'},
      auth=(self.id, self.password),
      data=json.dumps(data)
    )
    pprint.pprint(response.json())

if __name__ == '__main__':
  handler = Datasethandler()
  # handler.get_datasets()
  # handler.get_dataset(dataset_uuid='7c02c4b9-2147-4282-b7a9-db09ca934465')
  # handler.search_dataset(name='roishi-sample', datatype_name='chatbot-train')
  handler.create_dataset(name="roishi-sample-temp", datatype_uuid='494c8b2f-44da-4e0d-8b45-088d51892b32')