import asyncio
import logging
from nats.js.api import StreamConfig, DiscardPolicy
from nats.js.errors import NotFoundError, BadRequestError, ServerError
from serverish.connection import ConnectionNATS
from serverish.base import StatusEnum
from oca_nats_config.singleton_config import SingletonConfig

logger = logging.getLogger(__name__.rsplit('.')[-1])


class BuildStreams:

    def __init__(self):
        self.port = []
        self.host = []
        self.protocol = []
        nats_servers = SingletonConfig.get_config()["NATS"]
        for server in nats_servers:
            self.port.append(server["port"].get())
            self.host.append(server["host"].get())
            self.protocol.append(server["protocol"].get())

        self.streams = SingletonConfig.get_config()["STREAMS"].get()

    async def build_streams(self):
        cnc = ConnectionNATS(port=self.port, host=self.host)
        try:
            timeout = 10
            await asyncio.wait_for(cnc.connect(), timeout)
        except asyncio.TimeoutError as e:
            await cnc.update_statuses(no_deduce=True)
            logger.error(f"Can not connect to nats server - check server is running {cnc.format_status()}")
            return
        nc = cnc.nc
        try:
            #  ------ check server is alve ------
            response = await cnc.diagnose()
            for key, status in response.items():
                if status != StatusEnum.ok:
                    logger.error(f"Can not connect witch nats server. '{key}' has status '{status}'")
                    return
            # -----------------------------------
            js = nc.jetstream()
            for name, setting in self.streams.items():
                c = StreamConfig(name=name,
                                 description=setting.get("Description", None),
                                 subjects=setting.get("Subjects", None),
                                 retention=setting.get("Retention", None),
                                 max_consumers=setting.get("MaxConsumers", None),
                                 max_msgs=setting.get("MaxMsgs", None),
                                 max_bytes=setting.get("MaxBytes", None),
                                 discard=setting.get("Discard", DiscardPolicy.OLD),
                                 max_age=setting.get("MaxAge", None),  # in seconds
                                 max_msgs_per_subject=setting.get("MaxMsgsPerSubject", -1),
                                 max_msg_size=setting.get("MaxMsgSize", -1),
                                 storage=setting.get("Storage", None),
                                 num_replicas=setting.get("Replicas", None),
                                 no_ack=setting.get("NoAck", False),
                                 duplicate_window=setting.get("Duplicates", 0),
                                 placement=setting.get("Placement", None),
                                 mirror=setting.get("Mirror", None),
                                 sources=setting.get("Sources", None),
                                 sealed=setting.get("Sealed", False),
                                 deny_delete=setting.get("DenyDelete", False),
                                 deny_purge=setting.get("DenyPurge", False),
                                 allow_rollup_hdrs=setting.get("AllowRollup", False),
                                 republish=setting.get("RePublish", None),
                                 allow_direct=setting.get("AllowDirect", None),
                                 mirror_direct=setting.get("MirrorDirect", None)
                                 )

                if await BuildStreams._is_stream_exist(js, c.name):
                    logger.info(f"Stream '{c.name}' already exist")
                    await self._update_stream(js=js, cfg=c)
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

    async def _update_stream(self, js, cfg):
        info = await js.stream_info(cfg.name)

        try:
            p = await js.update_stream(config=cfg)
            logger.info(f"Successfully update stream {cfg.name}")
        except ServerError as e:
            logger.error(f"Can not update stream '{cfg.name}'. Reason {e.description}")
        except BadRequestError as e:
            if e.err_code == 10025:
                logger.error(f"Stream '{cfg.name}' has invalid configuration")
            else:
                logger.error(f"Stream '{cfg.name}' when update get error: {e}")
