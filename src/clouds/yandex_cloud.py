from logging import getLogger
import os.path
from urllib.request import pathname2url
from typing import Dict, Optional, List, Any
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

    def _query_params(self, path, is_dir: bool = False, kwargs: Optional[Dict[str, int | str]] = None) -> str:
        if is_dir:
            remote_path = self.remote_dir_path
        else:
            filename = os.path.basename(path)
            logger.debug("Filename is %s", filename)
            remote_path = os.path.join(self.remote_dir_path, filename)

        logger.debug("Remote path is %s", remote_path)
        remote_path = pathname2url(remote_path)

        if kwargs is not None:
            return "&".join((
                f"path={remote_path}",
                *(f"{key}={value}" for key, value in kwargs.items())
            ))
        else:
            return f"path={remote_path}"

    def load(self, path, overwrite: bool = False):
        logger.info("Start uploading a file to yandex disk")

        url = "?".join((
            self.base_url,
            self._query_params(path, {"overwrite": "true" if overwrite else "false"}),
        ))
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
        logger.info("Start deleting the file from yandex disk")

        url = "?".join((
            self.base_url,
            self._query_params(filename, {"permanently": "true"}),
        ))
        response: Response = requests.delete(
            url,
            headers=self.headers
        )
        if response.status_code != 204:
            logger.error("Status code is %d (must be 204)."
                         " Response body:\n%s", response.status_code, str(response.json()))
            raise ValueError("Status code is not 204")
        logger.debug("Done")

    def get_info(self) -> List[Dict[str, Any]]:
        logger.info("Start getting info about remote dir.")
        items: List[Dict[str, Any]] = list()
        limit: int = 20
        offset: int = 0

        url = "?".join((
            "https://cloud-api.yandex.net/v1/disk/resources",
            self._query_params(self.remote_dir_path, is_dir=True, kwargs={"limit": limit, "offset": offset}),
        ))
        response: Response = requests.get(
            url,
            headers=self.headers
        )
        if response.status_code != 200:
            logger.error("Status code is %d (must be 200)."
                         " Response body:\n%s", response.status_code, str(response.json()))
            raise ValueError("Status code is not 200")

        data_json = response.json()["_embedded"]
        items.extend(data_json["items"])

        #
        if data_json["total"] > limit:
            logger.debug("There were more files than the limit=%s, making a repeat request...", limit)
            offset = limit
            limit = data_json["total"]

            url = "?".join((
                "https://cloud-api.yandex.net/v1/disk/resources",
                self._query_params(self.remote_dir_path, is_dir=True, kwargs={"limit": limit, "offset": offset}),
            ))
            response: Response = requests.get(
                url,
                headers=self.headers
            )
            if response.status_code != 200:
                logger.error("Status code is %d (must be 200)."
                             " Response body:\n%s", response.status_code, str(response.json()))
                raise ValueError("Status code is not 200")

            data_json = response.json()["_embedded"]
            items.extend(data_json["items"])

        logger.debug("Done")
        return items
