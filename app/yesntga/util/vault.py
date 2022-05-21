from io import FileIO
import os
from os.path import exists, sep, join
from typing import Any

class VaultFile:
    """PLease don't use this direcrtly """
    def __init__(self, filename, method):
        self.o = open(filename, method)
    def __enter__(self):
        return self.o
    def __exit__(self, type, value, traceback):
        self.o.close()

class Vault:
    """A simple resolver for Docker secrets.
    Can be initialized with arguments to read somewhere other than /run/secets."""
    def __init__(self, secret_path: str = "/run/secrets"):
        self.SECRET_PATH = secret_path

    def get(self, filename: str, default_value: Any = None, read_mode: str = "r"):
        """Gets the contents of a file in the SECRET_PATH (default /run/secrets) directory.
        Similar to dict.get(), it returns a given 'default value' or None if the file doesn't exist."""
        if exists(join(self.SECRET_PATH, filename)):
            with open(join(self.SECRET_PATH, filename), read_mode) as f:
                return f.read()
        else:
            return default_value

    def open(self, filename: str, read_mode: str = "r"):
        """Makes a VaultFile object that opens a file in SECRET_PATH. Identical to a normal file context.
        This should not be used as it doesn't check if the file exists. Instead, use get."""
        return VaultFile(join(self.SECRET_PATH, filename), read_mode)