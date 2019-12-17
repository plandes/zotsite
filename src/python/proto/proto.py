import logging
from zensols.actioncli import ClassImporter
from zensols.zotsite import AppConfig

logger = logging.getLogger(__name__)


def tmp():
    conf = AppConfig('test-resources/zotsite.conf')
    app = ClassImporter('zensols.zotsite.site.SiteExporter').instance(conf)
    app.tmp()


def main():
    logging.basicConfig(level=logging.WARNING)
    run = 1
    {1: tmp,
     }[run]()


main()
