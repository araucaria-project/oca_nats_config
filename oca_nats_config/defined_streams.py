from oca_nats_config.defined_streams_method import DefinedStreamsMethod
from oca_nats_config.stream_property import StreamProperty


class DefinedStreams(DefinedStreamsMethod):
    WEATHER_TEMPERATURE_01 = StreamProperty("weather_temperature_01", ["weather_temperature_01"])
    WEATHER_WIND_01 = StreamProperty("weather_wind_01", ["weather_wind_01"])
    WEATHER_WIND_DIR_01 = StreamProperty("weather_wind_dir_01", ["weather_wind_dir_01"])
    WEATHER_HUMIDITY_01 = StreamProperty("weather_humidity_01", ["weather_humidity_01"])
    WEATHER_RAIN_01 = StreamProperty("weather_rain_01", ["weather_rain_01"])
    WEATHER_SUN_LIGHT_01 = StreamProperty("weather_sun_light_01", ["weather_sun_light_01"])
    WEATHER_SKY_TEMPERATURE_01 = StreamProperty("weather_sky_temperature_01", ["weather_sky_temperature_01"])
    WATCHER_LEVEL_01 = StreamProperty("watcher_level_01", ["watcher_level_01"])
    WATCHER_LEVEL_02 = StreamProperty("watcher_level_02", ["watcher_level_02"])
    DIESEL_LEVEL_01 = StreamProperty("diesel_level_01", ["diesel_level_01"])
