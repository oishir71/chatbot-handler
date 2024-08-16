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

class DatasetRecordHandler(BaseHandler):
  '''
  DatasetのRecordに該当する部分を操作するためのAPI。
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

  def get_records(self, dataset_uuid: str):
    '''
    datasetに紐付けされているdataset recordのレコード一覧を取得する
    '''
    response = requests.get(
      '%s/%s/records/' % (self.base_url, dataset_uuid),
      auth=self.authorization
    )
    self.parse_response(response=response)
    pprint.pprint(response.json())

  def get_records_all(self, dataset_uuid: str):
    '''
    DatasetRecord内に存在する全てのレコードの一覧を取得
    '''
    response = requests.get(
      '%s/%s/records/all/' % (self.base_url, dataset_uuid),
      auth=self.authorization
    )
    self.parse_response(response=response)
    pprint.pprint(response.json())

  def get_record(self, dataset_uuid: str, record_uuid: str):
    '''
    record_uuidで指定されたレコードの詳細情報を取得
    '''
    response = requests.get(
      '%s/%s/records/%s/' % (self.base_url, dataset_uuid, record_uuid),
      auth=self.authorization
    )
    self.parse_response(response=response)
    pprint.pprint(response.json())

  def create_record(self, dataset_uuid: str, bodies: list[dict]):
    '''
    新規レコードの追加
    '''
    data = {'data': [{'body': body} for body in bodies]}
    response = requests.post(
      '%s/%s/records/' % (self.base_url, dataset_uuid),
      headers={'Content-Type': 'application/json'},
      auth=self.authorization,
      data=json.dumps(data)
    )
    self.parse_response(response=response)
    pprint.pprint(response.json())

  def delete_record(self, dataset_uuid: str, record_uuid: str):
    '''
    record_uuidで指定されたレコードの削除
    '''
    response = requests.delete(
      '%s/%s/records/%s/' % (self.base_url, dataset_uuid, record_uuid),
      auth=self.authorization
    )
    self.parse_response(response=response)

if __name__ == '__main__':
  dataset_uuid='7c02c4b9-2147-4282-b7a9-db09ca934465'
  record_uuid='7025de47-6bae-48c8-b40a-48a19341df70'

  handler = DatasetRecordHandler()
  handler.get_records(dataset_uuid=dataset_uuid)
  # handler.get_records_all(dataset_uuid=dataset_uuid)
  # handler.get_record(dataset_uuid=dataset_uuid, record_uuid=record_uuid)
  # handler.create_record(
  #   dataset_uuid=dataset_uuid,
  #   bodies=[
  #     {
  #       'correct_answer': '6279c718-a990-4d8f-9dd4-b494d5d2d31e',
  #       'for_train': True,
  #       'question': '上戸彩の通信会社について',
  #     },
  #     {
  #       'correct_answer': '6279c718-a990-4d8f-9dd4-b494d5d2d31e',
  #       'for_train': True,
  #       'question': 'ダンテカーバーの通信会社について',
  #     },
  #   ]
  # )
  handler.delete_record(dataset_uuid=dataset_uuid, record_uuid='bea1a4d2-3f13-47f3-86b5-2ed65e24f244')
  handler.get_records(dataset_uuid=dataset_uuid)