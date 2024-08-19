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

class CalculateAccuracyHandler(BaseHandler):
  '''
  Dataset group内のログデータからチャットボットインスタンスの正答率を算出する。
  '''
  def __init__(
    self,
    host_url='http://localhost:8000',
    id='admin',
    password='password',
    project_id='631a6a99-0b30-425a-bdf2-af4532ff9451',
  ):
    super().__init__(host_url=host_url, id=id, password=password, project_id=project_id)
    self.base_url = '%s/api/chatbot/v1.0/projects/%s/calculate-accuracy' % (host_url, project_id)
    self.authorization = (id, password)

  def get_accuracy(self, datagroups: list[str]):
    '''
    datgroupsに対し正答率を算出する
    '''
    data={'datasetgroups': datagroups}
    response = requests.post(
      self.base_url,
      headers={'Content-Type': 'application/json'},
      auth=self.authorization,
      data=json.dumps(data)
    )
    self.parse_response(response=response)
    pprint.pprint(response.json())

if __name__ == '__main__':
  handler = CalculateAccuracyHandler()
  handler.get_accuracy(datagroups=['70518ce1-5c19-46a9-8922-7c02c2462273'])