from pathlib import Path

from gensim.corpora import WikiCorpus
from gensim.test.utils import datapath
import urllib3
import pathlib
from tqdm import tqdm
import opencc
import string
import jieba
import sys

paths = [
    '\\\\wsl$\\Ubuntu\\home\\amash\\git\\semantle-zh\\research',
    '\\\\wsl$\\Ubuntu\\home\\amash\\git\\semantle-zh',
    '\\home\\amash\\git\\semantle-zh\\research',
    '\\home\\amash\\git\\semantle-zh',
    '//wsl$/Ubuntu/home/amash/git/semantle-zh/research'
    '//wsl$/Ubuntu/home/amash/git/semantle-zh/'
    'home/amash/git/semantle-zh/research'
    'home/amash/git/semantle-zh/'
]
for path in paths:
    if path not in sys.path:
        sys.path.append(path)

print(sys.path)
# from research.base import get_config
import json
import pathlib


def get_config(path=None):
    if path is None:
        path = pathlib.Path(__file__).parent.resolve() / pathlib.Path('config.json')
    path = pathlib.Path(path)
    with path.open() as f:
        config = json.load(f)
    return config

PRINTABLE = set(string.printable)
jieba.initialize()


def download(url: str, dump_path: Path):
    if dump_path.exists():
        print("skipping download. file exists")
        return
    chunk_size = 1024
    http = urllib3.PoolManager(cert_reqs='CERT_NONE')
    r = http.request('GET', url, preload_content=False)

    i=0
    with dump_path.open('wb') as out:
        pbar = tqdm(total=int(r.headers['Content-Length']), unit='B', unit_scale=True, desc='Downloading corpus')
        data = r.read(chunk_size)
        while data:
            i+=1
            out.write(data)
            pbar.update(len(data))
            data = r.read(chunk_size)
    pbar.close()
    r.release_conn()


def preprocess(converter, text:str) -> str:
    # simplify
    text = converter.convert(text)
    # ascii
    text = ''.join([x for x in text if x not in PRINTABLE]).strip()
    # segmentation
    cutall = False
    hmm = True
    text = ' '.join(jieba.cut(text.rstrip('\r\n'), cutall, hmm))
    return text

if __name__ == "__main__":
    config = get_config()
    WIKIFILE = config['WIKIFILE']
    CORPUS_OUTPUT = config['CORPUS_OUTPUT']
    url = f"https://dumps.wikimedia.org/zhwiki/latest/{WIKIFILE}"

    base_path= pathlib.Path(__file__).parent.resolve()

    bz_temp_dump_path = base_path / Path(WIKIFILE)
    download(url, bz_temp_dump_path)
    wiki = WikiCorpus(datapath(str(bz_temp_dump_path)), dictionary={})
    corpus_output = base_path / Path(CORPUS_OUTPUT)
    print("Starting to create wiki corpus")
    converter = opencc.OpenCC('t2s.json')
    with corpus_output.open('wb') as output:
        for i, text in tqdm(enumerate(wiki.get_texts(), start=1),desc="saving articles", unit='articles', mininterval=5) :
            article = " ".join(text)
            article = preprocess(converter, article)
            output.write(f"{article}\n".encode('utf-8'))
