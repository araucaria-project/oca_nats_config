import asyncio
import logging

from nats.js.api import StreamConfig
from nats.js.errors import NotFoundError, BadRequestError
from serverish.connection_nats import ConnectionNATS
from serverish.status import StatusEnum

from oca_nats_config.defined_streams import DefinedStreams
from oca_nats_config.ob_config import SingletonConfig


logger = logging.getLogger(__name__.rsplit('.')[-1])


class BuildStreams:

    def __init__(self):
        self.port = SingletonConfig.get_config()["NATS"]["port"].get()
        self.host = SingletonConfig.get_config()["NATS"]["host"].get()
        self.protocol = SingletonConfig.get_config()["NATS"]["protocol"].get()

    async def build_streams(self):
        cnc = ConnectionNATS(port=self.port, host=self.host)
        response = await cnc.diagnose()
        for key, status in response.items():
            if status != StatusEnum.ok:
                logger.error(f"Can not connect witch nats server. '{key}' has status '{status}'")
                return
        await cnc.connect()
        nc = cnc.nc
        js = nc.jetstream()

        try:
            for s in DefinedStreams.get_list_streams():
                c = StreamConfig(name=s, description=s.desc(), subjects=s.subject())

                if await BuildStreams._is_stream_exist(js, c.name):
                    logger.info(f"Stream '{c.name}' already exist")
                    continue
                try:
                    result = await js.add_stream(config=c)
                except BadRequestError as e:
                    if e.err_code == 10065:
                        logger.error(f"One of the subjects '{c.subjects}' is already used by other stream")
                        return
                    else:
                        logger.error(f"Get error when trying to create stream: {e}")
                        return
                logger.info(f"Successfully created stream '{c.name}'")
        finally:
            await nc.close()

    @staticmethod
    async def _is_stream_exist(js, name):
        try:
            await js.stream_info(name)
        except NotFoundError:
            return False
        return True
