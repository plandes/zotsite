import os
from zensols.actioncli import OneConfPerActionOptionsCli
from zensols.actioncli import Config
from zensols.zotsite import SiteExporter

CONF_ENV_VAR = 'ZOTSITERC'


class ConfAppCommandLine(OneConfPerActionOptionsCli):
    def __init__(self):
        if CONF_ENV_VAR in os.environ:
            default_config_file = os.environ[CONF_ENV_VAR]
        else:
            default_config_file = '%s/.zotsiterc' % os.environ['HOME']
        datdir_op = ['-d', '--datadir', False,
                     {'dest': 'data_dir', 'metavar': 'FILE',
                      'help': 'the location of the Zotero data directory'}]
        outdir_op = ['-o', '--outputdir', True,
                     {'dest': 'out_dir', 'metavar': 'DIRECTORY',
                      'help': 'the directory to output the website'}]
        cnf = {'executors':
               [{'name': 'exporter',
                 'executor': lambda params: SiteExporter(**params),
                 'actions': [{'name': 'print',
                              'meth': 'print_structure',
                              'opts': [datdir_op]},
                             {'name': 'tmp'},
                             {'name': 'export',
                              'opts': [datdir_op, outdir_op]}]}],
               'config_option': {'name': 'config',
                                 'expect': False,
                                 'opt': ['-c', '--config', False,
                                         {'dest': 'config', 'metavar': 'FILE',
                                          'default': default_config_file,
                                          'help': 'configuration file'}]},
               'whine': 1}
        super(ConfAppCommandLine, self).__init__(
            cnf, pkg_dist='zensols.zotsite')

    def _create_config(self, conf_file, default_vars):
        defs = {}
        defs.update(default_vars)
        defs.update(os.environ)
        return Config(config_file=conf_file, default_vars=defs)


def main():
    cl = ConfAppCommandLine()
    cl.invoke()
