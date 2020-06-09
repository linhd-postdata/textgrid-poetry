#!/usr/bin/env python
# -*- coding: utf-8 -*-
# !pip install -q requests-html tqdm
import argparse
import json
import os
import time
import sys
import zipfile
from collections import Counter
from pathlib import Path

import requests
from requests_html import HTML
from tqdm.auto import tqdm


def download(download_list, download_files):
    print("Downloading:")
    for url, filename in zip(*[download_list, download_files]):
        chunk_size = 1024
        stream = requests.get(url, stream=True)
        bar_format = '{l_bar}{bar}| [{elapsed}<{remaining}, {rate_fmt}{postfix}]'
        with open(filename, 'wb') as file:
            progress = tqdm(
                desc=f"- {filename}",
                unit="B",
                bar_format=bar_format,
                total=int(stream.headers['Content-Length']))
            for chunk in stream.iter_content(chunk_size=chunk_size):
                if chunk: # filter out keep-alive new chunks
                    progress.update(len(chunk))
                    file.write(chunk)
    return download_files


def parse(files, json_folder="json"):
    poems_counter = 0
    stanza_counter = 0
    line_counter = 0
    authors_works = {}
    print("Parsing:")
    for zip_file in files:
        with zipfile.ZipFile(zip_file, "r") as unzip_file:
            for filename in tqdm(unzip_file.namelist(), desc=f"- {zip_file}"):
                if not filename.endswith(".xml"):
                    continue
                data = unzip_file.read(filename)
                chunk = HTML(html=data)
                poems = chunk.find("tei[n*=Gedichte]")
                if not len(poems):
                    continue
                author = chunk.find("bibl author", first=True).text
                if author not in authors_works:
                    authors_works[author] = []
                try:
                    author_ref = chunk.find(
                        "bibl author", first=True
                    ).attrs["key"]
                except:
                    author_ref = None
                idno = chunk.find("idno", first=True).text
                author_poems = []
                for poem in tqdm(poems, desc=author, leave=False):
                    title = poem.find("titleStmt title", first=True).text
                    publication_date = poem.find(
                        "biblFull publicationStmt date", first=True
                    )
                    creation_date = poem.find(
                        "profileDesc creation date", first=True
                    )
                    if publication_date and "when" in publication_date.attrs:
                        date = publication_date.attrs["when"]
                        dateType = "publicationDate"
                    elif creation_date and "notAfter" in creation_date.attrs:
                        date = (
                            f"{creation_date.attrs.get('notBefore', '')}"
                            f"-{creation_date.attrs['notAfter']}"
                        )
                        dateType = "creationDate"
                    else:
                        date = None
                    poems_counter += 1
                    poem_stanzas = []
                    for stanza in poem.find("lg"):
                        stanza_counter += 1
                        stanza_lines = []
                        for line in stanza.find("l"):
                            line_counter += 1
                            stanza_lines.append(" ".join(line.text.split("\n")))
                        poem_stanzas.append(stanza_lines)
                    if poem_stanzas:
                        authors_works[author].append({
                            "author": author,
                            "authorRef": author_ref,
                            dateType: date,
                            "title": title,
                            "text": poem_stanzas
                        })
    for author_code, author_works in authors_works.items():
        with open(json_folder / f"{author_code}.json", "w") as author_json:
            json.dump(author_works, author_json, indent=4)


def build(json_folder, corpus_file):
    corpus = []
    for json_file in tqdm(list(json_folder.rglob("*.json")), "Building"):
        corpus.extend(json.loads(json_file.open().read()))
    with open(corpus_file, "w") as corpus_json:
        json.dump(corpus, corpus_json, indent=4)
    counter = Counter()
    author_set = set()
    stanza_counter = 0
    line_counter = 0
    word_counter = 0
    for work in corpus:
        author_set.add(work["author"])
        for stanza in work["text"]:
            stanza_counter += 1
            for line in stanza:
                counter.update([len(line)])
                line_counter += 1
                word_counter += len(line.split())
    print("Statistics\n----------")
    print("- Authors:", len(author_set))
    print("- Works:", len(corpus))
    print("- Stanzas:", stanza_counter)
    print("- Verses:", line_counter)
    print("- Words:", word_counter)
    print("- Characters:", sum(k * v for k, v in counter.items()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        "Generates a JSON corpus from the poetry part of TextGrid "
        "(https://textgrid.de/en/digitale-bibliothek)"
    )
    download_url_base = "https://textgrid.de/fileadmin/digitale-bibliothek"
    download_files = (
        "literatur-nur-texte-1.zip",
        "literatur-nur-texte-2.zip"
    )
    download_list = tuple(
        f"{download_url_base}/{download_file}"
        for download_file in download_files
    )
    parser.add_argument("files", type=str, nargs="*",
        help=f"Zip file names containing the corpus {download_files}")
    parser.add_argument("-d", "--download", action='store_true', default=False,
        help=f"Download the zip files containing the corpus {download_list}")
    parser.add_argument("-np", "--no-parse", action='store_true', default=False,
        help=f"Parse the content of the zip files")
    parser.add_argument("--json-folder",
        help="path to parsed json content. "
        "Defaults to './json'",
        default="json")
    parser.add_argument("--corpus-file",
        help="path to generated json corpus. "
                "Defaults to './textgrid-poetry.json'",
        default="textgrid-poetry.json")
    args = parser.parse_args()
    if args.download:
        files = download(download_list, download_files)
    else:
        files = args.files
    if not args.no_parse:
        parse(corpus_file=args.corpus_file, files=files,
              json_folder=Path(args.json_folder))
    build(json_folder=Path(args.json_folder), corpus_file=args.corpus_file)
