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

# Handmade module
from base_handler import BaseHandler

class Datasethandler(BaseHandler):
  '''
  Datasetを操作するためのクラス。
  '''
  def __init__(
    self,
    host_url='http://localhost:8000',
    id='admin',
    password='password',
    project_id='631a6a99-0b30-425a-bdf2-af4532ff9451'
  ):
    super().__init__(host_url=host_url, id=id, password=password, project_id=project_id)
    self.base_url = '%s/api/datarepository/datasets' % (host_url)
    self.authorization = (id, password)

  def get_datasets(self):
    '''
    datasetの一覧を取得する
    '''
    response = requests.get(
      '%s/' % (self.base_url),
      auth=self.authorization
    )
    self.parse_response(response=response)
    pprint.pprint(response.json())

  def get_dataset(self, dataset_uuid: str):
    '''
    dataset_uuidに対応するdatasetを取得
    '''
    response = requests.get(
      '%s/%s/' % (self.base_url, dataset_uuid),
      auth=self.authorization
    )
    self.parse_response(response=response)
    pprint.pprint(response.json())

  def search_dataset(self, name: str, datatype_name: str):
    '''
    datasetを検索する
    '''
    data = {'name': name, 'datatype_name': datatype_name}
    response = requests.post(
      '%s/search/' % (self.base_url),
      headers={'Content-Type': 'application/json'},
      auth=self.authorization,
      data=json.dumps(data)
    )
    self.parse_response(response=response)
    pprint.pprint(response.text)

  def create_dataset(self, name: str, datatype_uuid: str):
    '''
    datasetを新規に作成する
    '''
    data = {'name': name, 'project': self.project_id, 'datatype': datatype_uuid}
    response = requests.post(
      '%s/' % (self.base_url),
      headers={'Content-Type': 'application/json'},
      auth=self.authorization,
      data=json.dumps(data)
    )
    self.parse_response(response=response)
    pprint.pprint(response.json())

  def delete_dataset(self, dataset_uuid: str):
    '''
    datasetを削除する
    '''
    response = requests.delete(
      '%s/%s/' % (self.base_url, dataset_uuid),
      auth=self.authorization
    )
    self.parse_response(response=response)

  def export_dataset(self, dataset_uuid: str):
    '''
    datasetに紐づくdataset recordに関する情報を出力する
    '''
    data = {'format': 'csv'}
    response = requests.post(
      '%s/%s/export/' % (self.base_url, dataset_uuid),
      headers={'Content-Type': 'application/json'},
      auth=self.authorization,
      data=json.dumps(data)
    )
    self.parse_response(response=response)
    pprint.pprint(response.content)

if __name__ == '__main__':
  handler = Datasethandler()
  handler.get_datasets()
  handler.get_dataset(dataset_uuid='7c02c4b9-2147-4282-b7a9-db09ca934465')
  # handler.search_dataset(name='roishi-sample', datatype_name='chatbot-train')
  # handler.create_dataset(name="roishi-sample-temp", datatype_uuid='494c8b2f-44da-4e0d-8b45-088d51892b32')
  # handler.delete_dataset(dataset_uuid='2dd162db-805c-41ec-b5b9-75e96a1e1576')
  handler.export_dataset(dataset_uuid='7c02c4b9-2147-4282-b7a9-db09ca934465')