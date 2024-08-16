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

  def get_datasets(self) -> list[dict]:
    '''
    datasetの一覧を取得する
    '''
    response = requests.get(
      '%s/' % (self.base_url),
      auth=self.authorization
    )
    self.parse_response(response=response)
    datasets = response.json()
    self.pprint_logger(object=datasets)
    return datasets

  def get_dataset(self, dataset_uuid: str) -> dict:
    '''
    dataset_uuidに対応するdatasetを取得
    '''
    response = requests.get(
      '%s/%s/' % (self.base_url, dataset_uuid),
      auth=self.authorization
    )
    self.parse_response(response=response)
    dataset = response.json()
    self.pprint_logger(object=dataset)
    return dataset

  def search_dataset(self, name: str, datatype_name: str) -> list[dict]:
    '''
    datasetを検索する、name & datatype_nameに部分一致のdatasetも検索にかかる
    '''
    data = {'name': name, 'datatype_name': datatype_name}
    response = requests.post(
      '%s/search/' % (self.base_url),
      headers={'Content-Type': 'application/json'},
      auth=self.authorization,
      data=json.dumps(data)
    )
    self.parse_response(response=response)
    datasets = response.json()
    self.pprint_logger(object=datasets)
    return datasets

  def create_dataset(self, name: str, datatype_uuid: str) -> list[dict]:
    '''
    datasetを新規に作成する。戻り値で存在するすべてのdatasetを返す。
    '''
    data = {'name': name, 'project': self.project_id, 'datatype': datatype_uuid}
    response = requests.post(
      '%s/' % (self.base_url),
      headers={'Content-Type': 'application/json'},
      auth=self.authorization,
      data=json.dumps(data)
    )
    self.parse_response(response=response)
    datasets = response.json()
    self.pprint_logger(object=datasets)
    return datasets

  def delete_dataset(self, dataset_uuid: str) -> None:
    '''
    datasetを削除する
    '''
    response = requests.delete(
      '%s/%s/' % (self.base_url, dataset_uuid),
      auth=self.authorization
    )
    self.parse_response(response=response)

  def delete_dataset_by_name(self, name: str) -> None:
    datasets = self.get_datasets()
    for dataset in datasets:
      if dataset.get('name') == name:
        self.delete_dataset(dataset_uuid=dataset.get('id'))

  def export_dataset(self, dataset_uuid: str) -> str:
    '''
    dataset_uuidを持つdatasetに紐づくdataset recordに関する情報を出力する
    '''
    data = {'format': 'csv'}
    response = requests.post(
      '%s/%s/export/' % (self.base_url, dataset_uuid),
      headers={'Content-Type': 'application/json'},
      auth=self.authorization,
      data=json.dumps(data)
    )
    self.parse_response(response=response)
    content = response.content
    self.pprint_logger(object=content)
    return content

  def export_dataset_by_name(self, name: str) -> list[str]:
    '''
    nameを持つdatasetに紐づくdataset recordに関する情報を出力する
    '''
    contents = []
    datasets = self.get_datasets()
    for dataset in datasets:
      if dataset.get('name') == name:
        contents.append(self.export_dataset(dataset_uuid=dataset.get('id')))
    return contents

if __name__ == '__main__':
  handler = Datasethandler()
  # handler.get_datasets()
  # handler.get_dataset(dataset_uuid='7c02c4b9-2147-4282-b7a9-db09ca934465')
  # handler.search_dataset(name='roishi-sample', datatype_name='chatbot-train')
  handler.create_dataset(name="roishi-sample-temp", datatype_uuid='494c8b2f-44da-4e0d-8b45-088d51892b32')
  # handler.delete_dataset_by_name(name='roishi-sample-temp')
  # handler.export_dataset(dataset_uuid='7c02c4b9-2147-4282-b7a9-db09ca934465')
  handler.export_dataset_by_name(name='roishi-sample-temp')