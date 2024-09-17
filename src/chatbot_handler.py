import os
import sys

# Logging
import logging

logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
handler_format = logging.Formatter(
    "%(asctime)s : [%(name)s - %(lineno)d] %(levelname)-8s - %(message)s"
)
stream_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)

# Handmade module
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.dialog_analyzer_handler import DialogAnalyzerHandler
from utils.dataset_group_handler import DatasetGroupHandler
from utils.dataset_handler import Datasethandler
from utils.dataset_record_handler import DatasetRecordHandler


class ChatbotHandler:
    def __init__(
        self,
        host_url="http://localhost:8000",
        id="admin",
        password="password",
        project_id="631a6a99-0b30-425a-bdf2-af4532ff9451",
    ):
        self.host_url = host_url
        self.id = id
        self.password = password
        self.project_id = project_id

        self.dialog_analyzer_handler = None
        self.dataset_group_handler = None
        self.dataset_handler = None
        self.answer_dataset_record_handler = None
        self.train_dataset_record_handler = None

        self.dialog_analyzer_uuid = "setme"
        self.dataset_group_uuid = "setme"
        self.answer_dataset_uuid = "setme"
        self.train_dataset_uuid = "setme"

    # Dataset group
    def setup_dataset_group_handler(self):
        self.dataset_group_handler = DatasetGroupHandler(
            host_url=self.host_url,
            id=self.id,
            password=self.password,
            project_id=self.project_id,
        )

    def create_dataset_group(self, name: str) -> dict:
        datagroup = self.dataset_group_handler.create_datasetgroup(name=name)
        self.dataset_group_uuid = datagroup.get("id")
        self.answer_dataset_uuid = datagroup.get("answer")
        self.train_dataset_uuid = datagroup.get("train")
        return datagroup

    def get_answer_records(self) -> list[dict]:
        return self.dataset_group_handler.get_answers(
            datasetgroup_uuid=self.dataset_group_uuid
        )

    def delete_dataset_group(self, datasetgroup_uuid: str) -> None:
        self.dataset_group_handler.delete_datasetgroup(
            datasetgroup_uuid=datasetgroup_uuid
        )

    def delete_dataset_group_by_name(self, name: str) -> None:
        self.dataset_group_handler.delete_datagroup_by_name(name=name)

    # Dataset
    def setup_dataset_handler(self):
        self.dataset_handler = Datasethandler(
            host_url=self.host_url,
            id=self.id,
            password=self.password,
            project_id=self.project_id,
        )

    # Dataset record
    def setup_answer_train_dataset_record_handler(self):
        self.answer_dataset_record_handler = DatasetRecordHandler(
            host_url=self.host_url,
            id=self.id,
            password=self.password,
            project_id=self.project_id,
            dataset_uuid=self.answer_dataset_uuid,
        )

        self.train_dataset_record_handler = DatasetRecordHandler(
            host_url=self.host_url,
            id=self.id,
            password=self.password,
            project_id=self.project_id,
            dataset_uuid=self.train_dataset_uuid,
        )

    def remove_answer_data_duplications(self, bodies: list[dict]):
        return self.answer_dataset_record_handler.remove_duplications_in_bodies(
            bodies=bodies, key="context"
        )

    def add_record_into_answer_dataset(self, bodies: list[dict]):
        self.answer_dataset_record_handler.create_records(bodies=bodies)

    def delete_record_from_answer_dataset(self, record_uuid: str):
        self.answer_dataset_record_handler.delete_record(record_uuid=record_uuid)

    def delete_records_from_answer_dataset(self, record_uuids: list[str]):
        for record_uuid in record_uuids:
            self.delete_record_from_answer_dataset(record_uuid=record_uuid)

    def get_answer_record_uuid_by_keyvalue(self, key: str, value: str):
        return self.answer_dataset_record_handler.get_record_uuid_by_keyvalue(
            key=key, value=value
        )

    def remove_train_data_duplications(self, bodies: list[dict]):
        return self.train_dataset_record_handler.remove_duplications_in_bodies(
            bodies=bodies, key="question"
        )

    def add_record_into_train_dataset(self, bodies: list[dict]):
        self.train_dataset_record_handler.create_records(bodies=bodies)

    def delete_record_from_train_dataset(self, record_uuid: str):
        self.train_dataset_record_handler.delete_record(record_uuid=record_uuid)

    def delete_records_from_train_dataset(self, record_uuids: list[str]):
        for record_uuid in record_uuids:
            self.delete_record_from_train_dataset(record_uuid=record_uuid)

    # Dialog analyzer
    def setup_dialog_analyzer_handler(self):
        self.dialog_analyzer_handler = DialogAnalyzerHandler(
            host_url=self.host_url,
            id=self.id,
            password=self.password,
            project_id=self.project_id,
        )

    def create_dialog_analyzer_instance(self, name: str):
        self.dialog_analyzer_handler.create_instance(
            name=name, datagroups=[self.dataset_group_uuid]
        )

    def deploy_dialog_analyzer_instance(self):
        self.dialog_analyzer_handler.deploy_instance(
            instance_id=self.dialog_analyzer_uuid
        )

    def undeploy_dialog_analyzer_instance(self):
        self.dialog_analyzer_handler.undeploy_instance(
            instance_id=self.dialog_analyzer_uuid
        )

    def infer(self, text: str):
        self.dialog_analyzer_handler.infer(
            instance_id=self.dialog_analyzer_uuid, text=text
        )

    def delete_dialog_analyzer_instance(self, name):
        self.dialog_analyzer_handler.delete_instance_by_name(name=name)

    # Dump
    def dump_chatbot_information(self, filename: str = "../histories/datagroup.csv"):
        with open(filename, mode="a") as f:
            f.weite(
                "%s,%s,%s,%s"
                % (
                    self.project_id,
                    self.dataset_group_uuid,
                    self.answer_dataset_uuid,
                    self.train_dataset_uuid,
                )
            )

    # Clean-up
    def cleanup_every_objects(self):
        self.dataset_handler.delete_dataset(dataset_uuid=self.answer_dataset_uuid)
        self.dataset_handler.delete_dataset(dataset_uuid=self.train_dataset_uuid)
        self.dataset_group_handler.delete_datasetgroup(
            datasetgroup_uuid=self.dataset_group_uuid
        )
        self.dialog_analyzer_handler.delete_instance(
            instance_id=self.dialog_analyzer_uuid
        )

        self.dialog_analyzer_uuid = "setme"
        self.dataset_group_uuid = "setme"
        self.answer_dataset_uuid = "setme"
        self.train_dataset_uuid = "setme"


if __name__ == "__main__":
    obj = ChatbotHandler()
    obj.setup_dataset_group_handler()
    obj.create_dataset_group(name="hogehoge-2")
    obj.setup_answer_train_dataset_record_handler()
    obj.add_record_into_answer_dataset(
        bodies=[
            {
                "title": "【衛星干渉事前計算】各種マスタ設定担当者の変更について",
                "context": '各種マスタ設定担当者の変更については、下記FAQをご参照の上、ご対応ください。\n▶<a href="https://open-ui.biz/cms/ou/faq/sat-intrf-precalculation/27192/">衛星干渉事前計算_各種マスタ設定担当者の変更について</a>',
            },
        ]
    )
    obj.add_record_into_train_dataset(
        bodies=[
            {
                "correct_answer": "6279c718-a990-4d8f-9dd4-b494d5d2d31e",
                "for_train": True,
                "question": "上戸彩の通信会社について",
            },
            {
                "correct_answer": "6279c718-a990-4d8f-9dd4-b494d5d2d31e",
                "for_train": True,
                "question": "ダンテカーバーの通信会社について",
            },
        ]
    )
    obj.setup_dialog_analyzer_handler()
    obj.create_dialog_analyzer_instance(name="hogehoge-da-2")
    obj.dump_chatbot_information()
    obj.cleanup_every_objects()
