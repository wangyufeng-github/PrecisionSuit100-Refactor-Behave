import time
from common.log import logger
from common.utils import Utils


def before_scenario(scenario,context):
    assert Utils().start_app()
    logger.info("软件已启动")


def after_scenario(scenario,context):
    assert Utils().stop_application()
    time.sleep(1)
    logger.info("软件已退出")