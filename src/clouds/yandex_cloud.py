import os.path
from urllib.request import pathname2url
from typing import Dict
import json

import requests
from requests import Response

from .cloud import Cloud


class YandexCloud(Cloud):

    def __init__(self, token: str, remote_dir_path: str):
        super().__init__(token, remote_dir_path)
        self.base_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        self.headers = {"Authorization": f"OAuth {token}"}

    def load(self, path):
        filename = os.path.basename(path)
        remote_path = os.path.join(self.remote_dir_path, filename)
        url = "?".join((self.base_url, f"path={pathname2url(remote_path)}"))
        print(url)
        response: Response = requests.get(
            url,
            headers=self.headers
        )

        data_dict = response.json()
        print(data_dict)
        if response.status_code != 200:
            raise ValueError(f"First request failed..., status code: {response.status_code}", )

        response = requests.put(
            data_dict["href"],
            headers=self.headers,
            data=open(path, "rb")
        )
        if not 200 <= response.status_code < 300:
            raise ValueError(f"Second request failed..., status code {response.status_code}")

    def reload(self, path):
        pass

    def delete(self, filename):
        pass

    def get_info(self):
        pass
