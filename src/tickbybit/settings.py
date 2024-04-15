import yaml
import logging

logger = logging.getLogger("tickbybit.settings")


def settings(dirpath: str) -> dict:
    filepatch = f'{dirpath}/settings.yaml'

    with open(filepatch) as fd:
        result = yaml.safe_load(fd)

        logger.info("Load settings %s", result)

        return result
