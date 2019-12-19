import logging
from zensols.actioncli import ClassImporter
from zensols.zotsite import AppConfig

logger = logging.getLogger(__name__)


def tmp():
    import os
    import zensols.zotsite.betterbib
    conf = AppConfig('test-resources/zotsite.conf', default_vars=os.environ)
    ci = ClassImporter('zensols.zotsite.betterbib.BetterBibtexMapper')
    ci.set_log_level(logging.DEBUG)
    app = ci.instance(conf.data_dir)
    app.tmp()


def main():
    logging.basicConfig(level=logging.WARNING)
    run = 1
    {1: tmp,
     }[run]()


main()
