import os
import sys
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

# Handmade module
sys.path.append(os.pardir)
from utils.dialog_analyzer_handler import DialogAnalyzerHandler
from utils.dataset_group_handler import DatasetGroupHandler
from utils.dataset_handler import Datasethandler
from utils.dataset_record_handler import DatasetRecordHandler

class ChatbotHandler:
  def __init__(self):
    self.host_url = 'http://localhost:8000'
    self.id = 'admin'
    self.password = 'password'
    self.project_id = '631a6a99-0b30-425a-bdf2-af4532ff9451'
    self.dataset_uuid = '7c02c4b9-2147-4282-b7a9-db09ca934465'

    self.dialog_analyzer_handler = None
    self.dataset_group_handler = None
    self.dataset_handler = None
    self.dataset_record_handler = None

  def get_datasetgroup_from_dialog_analyzer(self):
    '''
    TODO: dataset groupのidを取得する方法を見つける必要あり
    dialog analyzerから対応するdataset groupのidを取得する
    '''
    self.dialog_analyzer_handler()

  def get_dataset_ids_from_chatbot_datasetgroup(self, datasetgroup_uuid: str):
    '''
    dataset groupから対応するdatasetのidを取得する
    '''
    datasetgroup = self.dataset_group_handler.get_datasetgroup(datasetgroup_uuid=datasetgroup_uuid)
    return {name: datasetgroup.get(name) for name in ['answer', 'train', 'log']}

  def add_training_data_to_dataset(self, bodies: list):
    '''
    training用のdatasetにdataを追加する
    '''
    self.dataset_record_handler.create_records(bodies=bodies)

  def train_chatbot(self):
    '''
    TODO: chatbotを再度トレーニングする方法を探す必要あり
    chatbotを再度trainingする
    '''
    pass