import asyncio
import logging
from oca_nats_config.build_streams import BuildStreams

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('main')
logging.getLogger().setLevel(logging.INFO)


def main():
    asyncio.run(async_main())


async def async_main():
    bs = BuildStreams()
    await bs.build_streams()


if __name__ == '__main__':
    main()
