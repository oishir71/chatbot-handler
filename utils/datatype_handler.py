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

class DataTypeHandler(BaseHandler):
  '''
  DataTypeの形式を定義しているDataTypeを扱うためのクラス。
  '''
  def __init__(
    self,
    host_url='http://localhost:8000',
    id='admin',
    password='password',
  ):
    super().__init__(host_url=host_url, id=id, password=password)
    self.base_url = '%s/api/datarepository/datatypes' % (host_url)
    self.authorization = (id, password)

  def get_datatypes(self):
    '''
    DataTypeの一覧を取得
    '''
    response = requests.get(
      '%s/' % (self.base_url),
      auth=self.authorization
    )
    self.parse_response(response=response)
    datatypes = response.json()
    self.pprint_logger(object=datatypes)
    return datatypes

  def get_datatype(self, datatype_uuid: str):
    '''
    指定したDataTypeの詳細を取得
    '''
    response = requests.get(
      '%s/%s/' % (self.base_url, datatype_uuid),
      auth=self.authorization
    )
    self.parse_response(response=response)
    datatype = response.json()
    self.pprint_logger(object=datatype)
    return datatype

if __name__ == '__main__':
  handler = DataTypeHandler()
  handler.get_datatypes()
  handler.get_datatype(datatype_uuid='494c8b2f-44da-4e0d-8b45-088d51892b32')