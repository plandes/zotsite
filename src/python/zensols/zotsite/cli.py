import os
from zensols.actioncli import OneConfPerActionOptionsCliEnv
from zensols.actioncli import Config
from zensols.zotsite import SiteExporter


class ConfAppCommandLine(OneConfPerActionOptionsCliEnv):
    def __init__(self):
        coll_op = [None, '--collection', False,
                   {'dest': 'name_pat', 'metavar': 'DB PATTERN',
                    'help': 'regular expression pattern to match collections'}]
        datdir_op = ['-d', '--datadir', False,
                     {'dest': 'data_dir', 'metavar': 'FILE',
                      'help': 'the location of the Zotero data directory'}]
        outdir_op = ['-o', '--outputdir', True,
                     {'dest': 'out_dir', 'metavar': 'DIRECTORY',
                      'help': 'the directory to output the website'}]
        staticdir_op = [None, '--staticdirs', False,
                        {'dest': 'static_dirs', 'metavar': 'STRING',
                         'help': 'comma separated directories to ' +
                         'static files (you probably don\'t want to set)'}]
        cnf = {'executors':
               [{'name': 'exporter',
                 'executor': lambda params: SiteExporter(**params),
                 'actions': [{'name': 'print',
                              'meth': 'print_structure',
                              'opts': [datdir_op, coll_op]},
                             {'name': 'tmp'},
                             {'name': 'export',
                              'opts': [datdir_op, outdir_op, coll_op,
                                       staticdir_op]}]}],
               'config_option': {'name': 'config',
                                 'expect': False,
                                 'opt': ['-c', '--config', False,
                                         {'dest': 'config',
                                          'metavar': 'FILE',
                                          'help': 'configuration file'}]},
               'whine': 1}
        super(ConfAppCommandLine, self).__init__(
            cnf, config_env_name='zotsiterc', pkg_dist='zensols.zotsite')

    def _create_config(self, conf_file, default_vars):
        defs = {}
        defs.update(default_vars)
        defs.update(os.environ)
        return Config(config_file=conf_file, default_vars=defs)


def main():
    cl = ConfAppCommandLine()
    cl.invoke()
