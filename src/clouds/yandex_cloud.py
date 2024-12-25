from logging import getLogger
import os.path
from urllib.request import pathname2url
from typing import Dict
import json

import requests
from requests import Response

from .cloud import Cloud

logger = getLogger("main.yandex_cloud")


class YandexCloud(Cloud):

    def __init__(self, token: str, remote_dir_path: str):
        super().__init__(token, remote_dir_path)
        self.base_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        self.headers = {"Authorization": f"OAuth {token}"}

    def load(self, path, overwrite: bool = False):
        logger.info("Start uploading a file to yandex disk")

        filename = os.path.basename(path)
        logger.debug("Filename is %s", filename)
        remote_path = os.path.join(self.remote_dir_path, filename)
        logger.debug("Remote path is %s", remote_path)
        remote_path = pathname2url(remote_path)
        args: str = "path={remote_path}&overwrite={overwrite}".format(
            remote_path=remote_path,
            overwrite="true" if overwrite else "false",
        )

        url = "?".join((self.base_url, args))
        logger.debug("Getting href to uploading file...")
        response: Response = requests.get(
            url,
            headers=self.headers
        )

        data_dict = response.json()
        if response.status_code != 200:
            logger.error("Status code is %d (must be 200)."
                         " Response body:\n%s", response.status_code, str(data_dict))
            raise ValueError("Status code is not 200")

        logger.debug("Uploading file...")
        response = requests.put(
            data_dict["href"],
            headers=self.headers,
            data=open(path, "rb")
        )
        if response.status_code != 201 and response.status_code != 202:
            logger.error(
                "The download link was received, but the download failed.\n"
                "Status code - %d (must be 201 or 202). Response body:\n%s",
                response.status_code, str(response.json())
            )
            raise ValueError("The download link was received, but the download failed.")
        logger.debug("Done")

    def reload(self, path):
        self.load(path, overwrite=True)

    def delete(self, filename):
        pass

    def get_info(self):
        pass
