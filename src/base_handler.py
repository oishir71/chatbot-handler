import os

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
    if response.status_code == 200:
      logger.info('Successful termination.')
    elif response.status_code == 400:
      logger.error('Incorrect format request.')
    elif response.status_code == 403:
      logger.error('CSRF not set or invalid.')
    elif response.status_code == 404:
      logger.error('The specified object cannnot be found.')
    else:
      logger.error('Status code: %s - Text: %s' % (response.status_code, response.text))