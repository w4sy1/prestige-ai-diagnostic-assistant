import sys
import os
from normalization import normalize
from providers import LocalProvider
from runtime import entry,parser,read_json

def build():
    p=parser('LOCAL MODE — raport nie opuszcza komputera.')
    p.add_argument('--input');p.add_argument('--provider',choices=['local','openai'],default='local')
    p.add_argument('--model',default=os.environ.get('PRESTIGE_AI_MODEL','gpt-5-mini'))
    p.add_argument('--preview-send',action='store_true',help='Pokaż dokładny zestaw metryk dla zewnętrznego AI bez wysyłania')
    return p

def handle(a):
    if not a.input:raise ValueError('Podaj raport JSON.')
    metrics=normalize(read_json(a.input))
    if a.provider=='openai':
        from remote import analyze,payload
        if a.preview_send:return {'data_leaves_device':False,'preview':payload(metrics,a.model)}
        print('EXTERNAL AI: wybrane metryki zostaną wysłane do OpenAI; mogą obowiązywać opłaty API.',file=sys.stderr)
        return analyze(metrics,a.model)
    return LocalProvider().analyze(metrics)

if __name__=='__main__':sys.exit(entry(build,handle))
