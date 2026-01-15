from dishka import make_async_container

from src.core.config import load_configs, BaseConfigs
from src.core.ioc import setup_providers


def init_container():
    configs = load_configs()
    context = {
        BaseConfigs: configs.bot,
    }
    container = make_async_container(*setup_providers(), context=context)
    return configs, container