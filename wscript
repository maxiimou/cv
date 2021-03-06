from waflib import Logs
import os
import shutil
import re

topdir = '.'
bdldir = '%s/build/src' %topdir
outdir = '%s/target' % topdir
srcdir = '%s/src' % topdir

TEX_FILE_MATCHER = re.compile(r'.*\.tex$')
PDF_FILE_MATCHER = re.compile(r'.*\.pdf$')

def Colorpicker():
    notcolors = ['USE', 'cursor_on', 'cursor_off', 'NORMAL', 'BOLD']
    colors = [c for c in Logs.colors_lst if c not in notcolors]
    i = 0
    while True:
        if i == len(colors):
            i = 0
        yield colors[i]
        i += 1

def options(ctx):
    ctx.add_option('-d', '--debug',
        action='store_true', default=False,
        help='Outputs pdf errors while compiling')

def configure(conf):
    conf.load('tex')
    if not conf.env.LATEX:
        conf.fatal('The program LaTex is required')

def build(bld):
    colorpicker = Colorpicker()
    for filename in listfiles(srcdir, TEX_FILE_MATCHER):
        pdflatex(bld, os.path.join(srcdir, filename), color=next(colorpicker),
            name=filename)

def pdflatex(bld, src, color='NORMAL', name='pdflatex'):
    Logs.pprint(color, 'Compiling %s' % name)
    bld(
        features = 'tex',
        type     = 'pdflatex', # pdflatex or xelatex
        source   = src,  # mandatory, the source
        outs     = 'pdf', # 'pdf' or 'ps pdf'
        # deps     = 'crossreferencing.lst', # to give dependencies directly
        prompt   = 1 if bld.options.debug else 0, # 0 for the batch mode, 1 otherwise
        color=color,
        name=name
        )

def package(ctx):
    os.makedirs(outdir)
    for filename in listfiles(bdldir, PDF_FILE_MATCHER):
        shutil.copy(os.path.join(bdldir, filename),
                    os.path.join(outdir, filename))

def listfiles(dir, matcher=re.compile(r'.*')):
    return [filename for filename in os.listdir(dir) if matcher.match(filename)]
