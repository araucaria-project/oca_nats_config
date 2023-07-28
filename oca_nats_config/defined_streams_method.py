from abc import ABC
from typing import List

from oca_nats_config.stream_property import StreamProperty


class DefinedStreamsMethod(ABC):

    @classmethod
    def get_list_streams(cls) -> List[StreamProperty]:
        return [v for i, v in cls.__dict__.items() if i[:1] != '_' and isinstance(v, StreamProperty)]
