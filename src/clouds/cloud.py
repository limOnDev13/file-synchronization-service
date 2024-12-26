"""A module containing abstractions for working with cloud disks."""

from abc import ABC, abstractmethod


class Cloud(ABC):
    """
    An abstract class for working with the cloud disk API.

    Args:
        token (str) - Authorization token;
        remote_dir_path (str) - The path to the target folder in the cloud;
    """

    def __init__(self, token: str, remote_dir_path: str):
        self.token = token
        self.remote_dir_path = remote_dir_path

    @abstractmethod
    def load(self, path):
        """Upload the file to the storage."""
        pass

    @abstractmethod
    def reload(self, path):
        """Overwrite the file in the storage."""
        pass

    @abstractmethod
    def delete(self, filename):
        """Delete the file from the storage."""
        pass

    @abstractmethod
    def get_info(self):
        """Get info about files stored in remote storage."""
        pass
