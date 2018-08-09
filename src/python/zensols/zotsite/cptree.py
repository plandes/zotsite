import logging
import re
import os
from shutil import copy2, copystat

logger = logging.getLogger('zensols.zotsite.cptree')


class PatternFsCopier(object):
    """Copy files changing names for those that match on a regular expression.

    This was lifted directly from
      https://docs.python.org/3/library/shutil.html
    and then modified to change destination file names.
    """
    def __init__(self, fmatch_re, repl_re, dst_re):
        self.fmatch_re = re.compile(fmatch_re)
        self.repl_re = re.compile(repl_re)
        self.dst_re = dst_re

    def update_file(self, fname):
        if self.fmatch_re.match(fname):
            fname = self.repl_re.sub('_', fname)
        return fname

    def copytree(self, src, dst, symlinks=False):
        logger.debug('copying dir recursively {} -> {}'.format(src, dst))
        names = os.listdir(src)
        os.makedirs(dst)
        errors = []
        for name in names:
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            try:
                if symlinks and os.path.islink(srcname):
                    logger.debug('link: {} -> {}'.format(srcname, dstname))
                    linkto = os.readlink(srcname)
                    os.symlink(linkto, dstname)
                elif os.path.isdir(srcname):
                    logger.debug('dir: {} -> {}'.format(srcname, dstname))
                    self.copytree(srcname, dstname, symlinks)
                else:
                    dstname = self.update_file(dstname)
                    logger.debug('file: {} -> {}'.format(srcname, dstname))
                    copy2(srcname, dstname)
                # XXX What about devices, sockets etc.?
            except OSError as why:
                errors.append((srcname, dstname, str(why)))
            # catch the Error from the recursive copytree so that we can
            # continue with other files
            except Exception as err:
                errors.extend(err.args[0])
        try:
            copystat(src, dst)
        except OSError as why:
            # can't copy file access times on Windows
            if why.winerror is None:
                errors.extend((src, dst, str(why)))
        if errors:
            raise Exception(errors)
