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

class CalculateAccuracyHandler:
  '''
  TODO: 動かない。修正必要。
  '''
  def __init__(self):
    self.id = 'admin' # set me
    self.password = 'password' # set me
    self.project_id = '631a6a99-0b30-425a-bdf2-af4532ff9451' # set me
    self.host_url = 'http://localhost:8000'

  def get_accuracy(self, datagroupds: list[str]):
    data={'datasetgroups': datagroupds}
    response = requests.post(
      '%s/api/chatbot/v1.0/projects/%s/calculate-accuracy' % (self.host_url, self.project_id),
      auth=(self.id, self.password),
      data=json.dumps(data)
    )
    pprint.pprint(response.json())

if __name__ == '__main__':
  handler = CalculateAccuracyHandler()
  handler.get_accuracy(datagroupds=['70518ce1-5c19-46a9-8922-7c02c2462273'])