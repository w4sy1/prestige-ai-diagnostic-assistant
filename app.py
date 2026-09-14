import sys
from normalization import normalize
from providers import LocalProvider
from runtime import entry,parser,read_json

def build():
    p=parser('LOCAL MODE — raport nie opuszcza komputera.')
    p.add_argument('--input');p.add_argument('--provider',choices=['local'],default='local')
    return p

def handle(a):
    if not a.input:raise ValueError('Podaj raport JSON.')
    return LocalProvider().analyze(normalize(read_json(a.input)))

if __name__=='__main__':sys.exit(entry(build,handle))
