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

class DatasetGroupHandler:
  '''
  Chatbot用のデータセットグループを操作するためのクラス。
  '''
  def __init__(self):
    self.id = 'admin' # set me
    self.password = 'password' # set me
    self.project_id = '631a6a99-0b30-425a-bdf2-af4532ff9451' # set me
    self.host_url = 'http://localhost:8000'

  def get_datasetgroup_details(self):
    '''
    プロジェクト配下のデータセットグループを取得する
    '''
    response = requests.get(
      '%s/api/chatbot/v1.0/projects/%s/datasetgroups/' % (self.host_url, self.project_id),
      auth=(self.id, self.password),
    )
    pprint.pprint(response.json())

  def get_datasetgroup_detail(self, datasetgroup_uuid: str):
    '''
    hoge
    '''
    response = requests.get(
      '%s/api/chatbot/v1.0/projects/%s/datasetgroups/%s/' % (self.host_url, self.project_id, datasetgroup_uuid),
      auth=(self.id, self.password)
    )
    pprint.pprint(response.json())

  def create_datasetgroup(self, name: str):
    '''
    nameで指定した名前のデータグループを新規に作成する
    '''
    data={'name': name}
    response = requests.post(
      '%s/api/chatbot/v1.0/projects/%s/datasetgroups/' % (self.host_url, self.project_id),
      auth=(self.id, self.password),
      data=json.dumps(data)
    )
    pprint.pprint(response.json())

  def delete_datasetgroup(self, datasetgroup_uuid: str):
    '''
    UUIDに対応するデータグループを削除する
    '''
    response = requests.delete(
      '%s/api/chatbot/v1.0/projects/%s/datasetgroups/%s/' % (self.host_url, self.project_id, datasetgroup_uuid),
      auth=(self.id, self.password)
    )
    pprint.pprint(response.json())

  def get_answers(self, datasetgroup_uuid: str):
    '''
    UUIDに対応するデータグループが持つ解答データを取得する
    '''
    response = requests.get(
      '%s/api/chatbot/v1.0/projects/%s/datasetgroups/%s/answers/' % (self.host_url, self.project_id, datasetgroup_uuid),
      auth=(self.id, self.password)
    )
    pprint.pprint(response.json())

if __name__ == '__main__':
  datasetgroup_uuid = '70518ce1-5c19-46a9-8922-7c02c2462273'

  handler = DatasetGroupHandler()
  handler.get_datasetgroup_detail(datasetgroup_uuid=datasetgroup_uuid)
  handler.get_answers(datasetgroup_uuid=datasetgroup_uuid)