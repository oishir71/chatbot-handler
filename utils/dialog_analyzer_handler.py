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

class DialogAnalyzerHandler(BaseHandler):
  '''
  MLAPI基盤に搭載されているDialogAnalyzer v2.0を操作するためのクラス。
  '''
  def __init__(
    self,
    host_url='http://localhost:8000',
    id='admin',
    password='password',
    project_id='631a6a99-0b30-425a-bdf2-af4532ff9451'
  ):
    super().__init__(host_url=host_url, id=id, password=password, project_id=project_id)
    self.base_url = '%s/api/projects/%s/mlapi/dialog-analyzer-v2' % (host_url, project_id)
    self.authorization = (id, password)

  def get_instances(self) -> list[dict]:
    '''
    インスタンスの一覧を取得する.
    '''
    response = requests.get(
      self.base_url,
      auth=self.authorization
    )
    self.parse_response(response=response)
    instances = response.json().get('instances')
    logger.debug('Number of instances: %d' % (len(instances)))
    return instances

  def get_instance(self, instance_id: str) -> dict:
    '''
    instance_idで指定したインスタンスの詳細を取得する
    '''
    response = requests.get(
      '%s/%s' % (self.base_url, instance_id),
      auth=self.authorization
    )
    self.parse_response(response=response)
    instance = response.json()
    self.pprint_logger(object=instance)
    return instance

  def get_instance_by_name(self, name: str):
    instances = self.get_instances()
    for instance in instances:
      if instance.get('name') == name:
        return instance
    else:
      logger.error('No such instance was detected: "%s"' % (name))
    return None

  def deploy_instance(self, instance_id: str) -> dict:
    '''
    instance_idで指定したインスタンスを起動する
    '''
    response = requests.post(
      '%s/%s/deployment' % (self.base_url, instance_id),
      auth=self.authorization
    )
    self.parse_response(response=response)
    information = response.json()
    self.pprint_logger(object=information)
    return information

  def undeploy_instance(self, instance_id: str) -> dict:
    '''
    instance_idで指定したインスタンスを停止する
    '''
    response = requests.delete(
      '%s/%s/deployment' % (self.base_url, instance_id),
      auth=self.authorization
    )
    self.parse_response(response=response)
    information = response.json()
    self.pprint_logger(object=information)
    return information

  def create_instance(self, name: str, datagroups: list[str]):
    '''
    nameで指定した名前のインスタンスを新規に作成する
    '''
    data = {'name': name, 'project': datagroups}
    response = requests.post(
      '%s/train' % (self.base_url),
      headers = {'Content-Type': 'application/json'},
      auth = self.authorization,
      data = json.dumps(data),
    ),
    self.parse_response(response=response)
    pprint.pprint(response.json())

  def delete_instance(self, instance_id: str):
    '''
    instance_idで指定したインスタンスを削除する
    '''
    response = requests.delete(
      '%s/%s' % (self.base_url, instance_id),
      auth = self.authorization,
    )
    self.parse_response(response=response)
    pprint.pprint(response)

  def infer(self, instance_id: str, text: str):
    '''
    引数として渡されたテキストに対し推論を行う
    '''
    data = {'text': text}
    response = requests.post(
      '%s/%s/infer' % (self.base_url, instance_id),
      headers={'Content-Type': 'application/json'},
      auth = self.authorization,
      data = json.dumps(data)
    )
    self.parse_response(response=response)
    pprint.pprint(response.json())

if __name__ == '__main__':
  instance_id = '0qwknp4jrnu2yt3b'

  handler = DialogAnalyzerHandler()
  # print(handler.get_instance(instance_id=instance_id))
  # print(handler.get_instance_by_name(name='sample-local-oishir71'))
  # handler.get_instance_detail(instance_id=instance_id)
  handler.deploy_instance(instance_id=instance_id)
  # handler.infer(instance_id=instance_id, text='test')
  handler.undeploy_instance(instance_id=instance_id)