import asyncio
import logging
from oca_nats_config.build_streams import BuildStreams

logger = logging.getLogger(__name__.rsplit('.')[-1])


def main():
    asyncio.run(async_main())


async def async_main():
    bs = BuildStreams()
    await bs.build_streams()


if __name__ == '__main__':
    main()
