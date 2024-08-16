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

class DatasetGroupHandler(BaseHandler):
  '''
  Chatbot用のデータセットグループを操作するためのクラス。
  '''
  def __init__(
    self,
    host_url='http://localhost:8000',
    id='admin',
    password='password',
    project_id='631a6a99-0b30-425a-bdf2-af4532ff9451',
  ):
    super().__init__(host_url=host_url, id=id, password=password, project_id=project_id)
    self.base_url = '%s/api/chatbot/v1.0/projects/%s/datasetgroups' % (host_url, project_id)
    self.authorization = (id, password)

  def get_datasetgroup_details(self):
    '''
    プロジェクト配下のデータセットグループを取得する
    '''
    response = requests.get(
      '%s/' % (self.base_url),
      auth=self.authorization
    )
    self.parse_response(response=response)
    pprint.pprint(response.json())

  def get_datasetgroup_detail(self, datasetgroup_uuid: str):
    '''
    特定のデータセットグループの詳細を取得する
    '''
    response = requests.get(
      '%s/%s/' % (self.base_url, datasetgroup_uuid),
      auth=self.authorization
    )
    self.parse_response(response=response)
    pprint.pprint(response.json())

  def create_datasetgroup(self, name: str):
    '''
    nameで指定した名前のデータグループを新規に作成する
    '''
    data={'name': name}
    response = requests.post(
      '%s/' % (self.base_url),
      headers={'Content-Type': 'application/json'},
      auth=self.authorization,
      data=json.dumps(data)
    )
    self.parse_response(response=response)
    pprint.pprint(response.json())

  def delete_datasetgroup(self, datasetgroup_uuid: str):
    '''
    UUIDに対応するデータグループを削除する
    '''
    response = requests.delete(
      '%s/%s/' % (self.base_url, datasetgroup_uuid),
      auth=self.authorization
    )
    self.parse_response(response=response)
    pprint.pprint(response.json())

  def get_answers(self, datasetgroup_uuid: str):
    '''
    UUIDに対応するデータグループが持つ解答データを取得する
    '''
    response = requests.get(
      '%s/%s/answers/' % (self.base_url, datasetgroup_uuid),
      auth=self.authorization
    )
    self.parse_response(response=response)
    pprint.pprint(response.json())

if __name__ == '__main__':
  datasetgroup_uuid = '70518ce1-5c19-46a9-8922-7c02c2462273'

  handler = DatasetGroupHandler()
  handler.get_datasetgroup_details()
  handler.get_datasetgroup_detail(datasetgroup_uuid=datasetgroup_uuid)
  handler.get_answers(datasetgroup_uuid=datasetgroup_uuid)