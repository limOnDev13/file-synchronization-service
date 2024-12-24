from utils.files import search_files
from config.env_config import Config
from clouds.yandex_cloud import YandexCloud
from clouds.cloud import Cloud


if __name__ == "__main__":
    config = Config()
    print(config)
    cloud: YandexCloud = YandexCloud(config.token, config.remote_dir_path)
    print(cloud.headers)
    for file_path in search_files(config.target, depth=0):
        print(file_path)
        cloud.load(file_path)
        print("Done!")
