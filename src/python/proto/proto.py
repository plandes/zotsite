import logging
from zensols.actioncli import ClassImporter
from zensols.zotsite import AppConfig

logger = logging.getLogger(__name__)


def tmp():
    import os
    conf = AppConfig('test-resources/zotsite.conf', default_vars=os.environ)
    print(conf.get_option('data_dir'))
    app = ClassImporter('zensols.zotsite.site.SiteCreator').instance(conf)
    app.tmp()


def main():
    logging.basicConfig(level=logging.WARNING)
    run = 1
    {1: tmp,
     }[run]()


main()
