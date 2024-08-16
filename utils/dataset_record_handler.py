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
    project_id='631a6a99-0b30-425a-bdf2-af4532ff9451',
    dataset_uuid='7c02c4b9-2147-4282-b7a9-db09ca934465'
  ):
    super().__init__(host_url=host_url, id=id, password=password, project_id=project_id)
    self.base_url = '%s/api/datarepository/datasets/%s' % (host_url, dataset_uuid)
    self.authorization = (id, password)

  def get_records(self) -> list[dict]:
    '''
    datasetに紐付けされているdataset recordのレコード一覧を取得する
    '''
    response = requests.get(
      '%s/records/' % (self.base_url),
      auth=self.authorization
    )
    self.parse_response(response=response)
    records = response.json()
    self.pprint_logger(object=records)
    return records

  def get_record_payloads(self) -> list[dict]:
    records = self.get_records()
    return records.get('result')

  def get_record_information(self) -> dict:
    records = self.get_records()
    del records['result']
    return records

  def get_record(self, record_uuid: str) -> dict:
    '''
    record_uuidで指定されたレコードの詳細情報を取得
    '''
    response = requests.get(
      '%s/records/%s/' % (self.base_url, record_uuid),
      auth=self.authorization
    )
    self.parse_response(response=response)
    record = response.json()
    self.pprint_logger(object=record)
    return record

  def create_records(self, bodies: list[dict]) -> list[dict]:
    '''
    新規レコードの追加
    '''
    data = {'data': [{'body': body} for body in bodies]}
    response = requests.post(
      '%s/records/' % (self.base_url),
      headers={'Content-Type': 'application/json'},
      auth=self.authorization,
      data=json.dumps(data)
    )
    self.parse_response(response=response)
    records = response.json()
    self.pprint_logger(object=records)
    return records

  def delete_record(self, record_uuid: str) -> None:
    '''
    record_uuidで指定されたレコードの削除
    '''
    response = requests.delete(
      '%s/records/%s/' % (self.base_url, record_uuid),
      auth=self.authorization
    )
    self.parse_response(response=response)

  def delete_record_by_question(self, question: str) -> None:
    '''
    質問を元にレコードを削除する
    '''
    records = self.get_record_payloads()
    for record in records:
      print(record)
      if record.get('body').get('question') == question:
        self.delete_record(record_uuid=record.get('id'))
        logger.debug('Record Id: %s was deleted.' % (record.get('id')))

if __name__ == '__main__':
  record_uuid='7025de47-6bae-48c8-b40a-48a19341df70'

  handler = DatasetRecordHandler()
  handler.create_records(
    bodies=[
      {
        'correct_answer': '6279c718-a990-4d8f-9dd4-b494d5d2d31e',
        'for_train': True,
        'question': '上戸彩の通信会社について',
      },
      {
        'correct_answer': '6279c718-a990-4d8f-9dd4-b494d5d2d31e',
        'for_train': True,
        'question': 'ダンテカーバーの通信会社について',
      },
    ]
  )
  handler.delete_record_by_question(question='上戸彩の通信会社について')
  handler.delete_record_by_question(question='ダンテカーバーの通信会社について')
  handler.get_records()