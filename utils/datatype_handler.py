import os
import sys
import requests
from typing import Union

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
sys.path.append(os.path.dirname(__file__))
from base_handler import BaseHandler


class DataTypeHandler(BaseHandler):
    """
    DataTypeの形式を定義しているDataTypeを扱うためのクラス。
    """

    def __init__(
        self,
        host_url="http://localhost:8000",
        id="admin",
        password="password",
    ):
        super().__init__(host_url=host_url, id=id, password=password)
        self.base_url = "%s/api/datarepository/datatypes" % (host_url)
        self.authorization = (id, password)

    def get_datatypes(self) -> list[dict]:
        """
        DataTypeの一覧を取得
        """
        response = requests.get("%s/" % (self.base_url), auth=self.authorization)
        self.parse_response(response=response)
        datatypes = response.json()
        return datatypes

    def get_datatype(self, datatype_uuid: str) -> dict:
        """
        指定したDataTypeの詳細を取得
        """
        response = requests.get(
            "%s/%s/" % (self.base_url, datatype_uuid), auth=self.authorization
        )
        self.parse_response(response=response)
        datatype = response.json()
        return datatype

    def get_datatype_by_name(self, name: str) -> Union[dict, None]:
        datatypes = self.get_datatypes()
        for datatype in datatypes:
            if datatype.get("name") == name:
                return datatype
        else:
            logger.error("No such datatype was detected: %s" % (name))
        return None


if __name__ == "__main__":
    handler = DataTypeHandler()
    print(handler.get_datatypes())
    print(
        handler.get_datatype(datatype_uuid="494c8b2f-44da-4e0d-8b45-088d51892b32")
    )  # chatbot-train
    print(
        handler.get_datatype(datatype_uuid="258fe363-3fdc-442a-8642-93ba49e3b08d")
    )  # chatbot-answer
