"""A module for working with yandex disk."""

import os.path
from logging import getLogger
from typing import Any, Dict, List
from urllib.request import pathname2url

import requests
from requests import Response

from .cloud import Cloud

logger = getLogger("main.yandex_cloud")


class YandexCloud(Cloud):
    """A class for working with yandex disk."""

    def __init__(self, token: str, remote_dir_path: str):
        super().__init__(token, remote_dir_path)
        self.headers = {"Authorization": f"OAuth {token}"}

    @classmethod
    def _query_params(cls, kwargs: Dict[str, int | str]) -> str:
        """Collect request parameters from kwargs."""
        return "&".join((f"{key}={value}" for key, value in kwargs.items()))

    def load(self, path, overwrite: bool = False):
        """Upload the file to the storage."""
        logger.debug("Start uploading a file to yandex disk\npath=%s", path)

        filename: str = os.path.basename(path)
        base_url: str = "https://cloud-api.yandex.net/v1/disk/resources/upload"

        url = "?".join(
            (
                base_url,
                self._query_params(
                    {
                        "path": pathname2url(
                            os.path.join(self.remote_dir_path, filename)
                        ),
                        "overwrite": "true" if overwrite else "false",
                    }
                ),
            )
        )
        logger.debug("Getting href to uploading file...")
        response: Response = requests.get(url, headers=self.headers)

        data_dict = response.json()
        if response.status_code != 200:
            logger.error(
                "Status code is %d (must be 200).\npath=%s\nResponse body:\n%s",
                response.status_code,
                path,
                str(data_dict),
            )
            raise ValueError("Status code is not 200")

        logger.debug("Uploading file...")
        response = requests.put(
            data_dict["href"], headers=self.headers, data=open(path, "rb")
        )
        if response.status_code != 201 and response.status_code != 202:
            logger.error(
                "The download link was received, but the download failed.\n"
                "Status code - %d (must be 201 or 202).\npath=%s\nResponse body:\n%s",
                response.status_code,
                path,
                str(response.json()),
            )
            raise ValueError("The download link was received, but the download failed.")
        logger.debug("Done")

    def reload(self, path):
        """Overwrite the file in the storage."""
        self.load(path, overwrite=True)

    def delete(self, filename):
        """Delete the file from the storage."""
        logger.debug("Start deleting the file from yandex disk\nfilename=%s", filename)

        base_url: str = "https://cloud-api.yandex.net/v1/disk/resources"

        url = "?".join(
            (
                base_url,
                self._query_params(
                    {
                        "path": pathname2url(
                            os.path.join(self.remote_dir_path, filename)
                        ),
                        "permanently": "true",
                    }
                ),
            )
        )
        response: Response = requests.delete(url, headers=self.headers)
        if response.status_code != 204:
            logger.error(
                "Status code is %d (must be 204).\nfilename=%s\nResponse body:\n%s",
                response.status_code,
                filename,
                str(response.json()),
            )
            raise ValueError("Status code is not 204")
        logger.debug("Done")

    def get_info(self) -> List[Dict[str, Any]]:
        """Get info about files stored in remote storage."""
        logger.debug("Start getting info about remote dir.")
        items: List[Dict[str, Any]] = list()
        limit: int = 20
        offset: int = 0
        base_url: str = "https://cloud-api.yandex.net/v1/disk/resources"

        url = "?".join(
            (
                base_url,
                self._query_params(
                    {
                        "path": pathname2url(self.remote_dir_path),
                        "limit": limit,
                        "offset": offset,
                    }
                ),
            )
        )
        response: Response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            logger.error(
                "Status code is %d (must be 200).\nResponse body:\n%s",
                response.status_code,
                str(response.json()),
            )
            raise ValueError("Status code is not 200")

        data_json = response.json()["_embedded"]
        items.extend(data_json["items"])

        #
        if data_json["total"] > limit:
            logger.debug(
                "There were more files than the limit=%s, making a repeat request...",
                limit,
            )
            offset = limit
            limit = data_json["total"]

            url = "?".join(
                (
                    base_url,
                    self._query_params(
                        {
                            "path": pathname2url(self.remote_dir_path),
                            "limit": limit,
                            "offset": offset,
                        }
                    ),
                )
            )
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                logger.error(
                    "Status code is %d (must be 200).\nResponse body:\n%s",
                    response.status_code,
                    str(response.json()),
                )
                raise ValueError("Status code is not 200")

            data_json = response.json()["_embedded"]
            items.extend(data_json["items"])

        logger.debug("Done")
        return items
