import os
import logging
import multiprocessing
import confuse
from threading import Lock

logger = logging.getLogger(__name__.rsplit('.')[-1])


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class SingletonConfig(metaclass=SingletonMeta):
    app_name = 'oca_nats_config'
    _DEFAULT_CONFIG_FILE_NAME = 'config.yaml'
    _SECRET_CONFIG_FILE_NAME = '.secrets.yaml'
    _config: confuse.ConfigView = None
    additional_files = []

    @classmethod
    def get_config(cls, add_files: list = None, rebuild=False) -> confuse.ConfigView:
        """
        Returns configuration singleton
        """
        with multiprocessing.Lock():
            if cls._config is None or rebuild:
                if add_files is not None:
                    cls.additional_files += add_files
                cls._config = cls._parse_config_files()
        return cls._config

    @classmethod
    def add_config_file(cls, f: str):
        with multiprocessing.Lock():
            cls.additional_files += [f]

    @classmethod
    def add_config_file_from_config_dir(cls, f: str):
        cls.add_config_file(os.path.join(cls.get_path_to_config_dir(), f))

    @staticmethod
    def _get_inst_dir():
        thisfile = __file__
        thisdir = os.path.dirname(thisfile)
        return thisdir

    @classmethod
    def get_package_file_path(cls, f):
        """
        Returns absolute path to file in package directory.
        """
        return os.path.join(cls._get_inst_dir(), f)

    @classmethod
    def get_path_to_config_dir(cls):
        return os.path.join(cls._get_inst_dir(), 'configuration')

    @classmethod
    def get_config_files(cls):
        return [
                   cls.get_package_file_path(cls._DEFAULT_CONFIG_FILE_NAME),
                   os.path.join(cls._get_inst_dir(), 'configuration', cls._DEFAULT_CONFIG_FILE_NAME),
                   os.path.join(cls._get_inst_dir(), 'configuration', cls._SECRET_CONFIG_FILE_NAME),
                   # /ob/configuration/config.yaml
               ] + cls.additional_files

    @classmethod
    def _parse_config_files(cls, files: list or None = None, parse_default_locations=True):
        """Parses set of config files"""
        fil = []
        if parse_default_locations:
            fil += [os.path.join(os.path.expanduser(d)) for d in cls.get_config_files()]
        if files is not None:
            fil += files
        config = confuse.Configuration(cls.app_name, read=False)
        for f in fil:
            logger.debug('Trying config: %s', f)
            try:
                source = confuse.YamlSource(f, optional=True)
                config.set(source)
                if len(source) > 0:
                    logger.info('Using config: %s', f)
                else:
                    logger.info('Empty config: %s', f)
            except confuse.ConfigReadError:
                logger.warning('Corrupted config: %s', f)
        return config
