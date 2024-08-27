import os
import requests
import pprint
import json
from typing import Union

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
from .base_handler import BaseHandler

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

  def get_datasetgroups(self) -> list[dict]:
    '''
    プロジェクト配下のデータセットグループを取得する
    '''
    response = requests.get(
      '%s/' % (self.base_url),
      auth=self.authorization
    )
    self.parse_response(response=response)
    datasetgroups = response.json()
    self.pprint_logger(object=datasetgroups)
    return datasetgroups

  def get_datasetgroup(self, datasetgroup_uuid: str) -> dict:
    '''
    特定のデータセットグループを取得する
    '''
    response = requests.get(
      '%s/%s/' % (self.base_url, datasetgroup_uuid),
      auth=self.authorization
    )
    self.parse_response(response=response)
    datasetgroup = response.json()
    self.pprint_logger(object=datasetgroup)
    return datasetgroup

  def get_datasetgroup_by_name(self, name: str) -> Union[dict, None]:
    '''
    特定の名前のデータセットグループを取得する
    '''
    datasetgroups = self.get_datasetgroups()
    for datasetgroup in datasetgroups:
      if datasetgroup.get('name') == name:
        return datasetgroup
    else:
      logger.error('No such datagroup was detected: "%s"' % (name))
    return None

  def create_datasetgroup(self, name: str) -> dict:
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
    datagroup = response.json()
    self.pprint_logger(object=datagroup)
    return datagroup

  def delete_datasetgroup(self, datasetgroup_uuid: str) -> None:
    '''
    UUIDに対応するデータグループを削除する
    '''
    response = requests.delete(
      '%s/%s/' % (self.base_url, datasetgroup_uuid),
      auth=self.authorization
    )
    self.parse_response(response=response)

  def delete_datagroup_by_name(self, name: str) -> None:
    datagroup = self.get_datasetgroup_by_name(name=name)
    if not datagroup is None:
      self.delete_datasetgroup(datasetgroup_uuid=datagroup.get('id'))

  def get_answers(self, datasetgroup_uuid: str) -> list[dict]:
    '''
    UUIDに対応するデータグループが持つ解答データを取得する
    '''
    response = requests.get(
      '%s/%s/answers/' % (self.base_url, datasetgroup_uuid),
      auth=self.authorization
    )
    self.parse_response(response=response)
    answers = response.json()
    self.pprint_logger(object=answers)
    return answers

if __name__ == '__main__':
  datasetgroup_uuid = '70518ce1-5c19-46a9-8922-7c02c2462273'

  handler = DatasetGroupHandler()
  handler.get_datasetgroups()
  handler.get_datasetgroup(datasetgroup_uuid=datasetgroup_uuid)
  datagroup = handler.create_datasetgroup(name='aho-no-1')
  handler.get_answers(datasetgroup_uuid=datasetgroup_uuid)