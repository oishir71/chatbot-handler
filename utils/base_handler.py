import os
import pprint

# Logging
import logging
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
handler_format = logging.Formatter('%(asctime)s : [%(name)s - %(lineno)d] %(levelname)-8s - %(message)s')
stream_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)

class BaseHandler:
  '''
  Chatbotを構成する各要素の元となる基本的なクラス
  '''
  def __init__(
    self,
    host_url='http://localhost:8000',
    id='admin',
    password='password',
    project_id='631a6a99-0b30-425a-bdf2-af4532ff9451'
  ):
    self.host_url = host_url
    self.id = id
    self.password = password
    self.project_id = project_id

  def parse_response(self, response):
    if response.status_code in [200, 201, 204]:
      logger.info('正常終了')
    else:
      logger.error('ステータス: %s - %s' % (response.status_code, response.text))

  @staticmethod
  def pprint_logger(object):
    for line in pprint.pformat(object, width=150).split('\n'):
      logger.info(line)