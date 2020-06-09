# TextGrid Poetry Corpus (German)

This corpus is a subset in JSON format of the available poems in [TexGrid](https://textgrid.de/en/digitale-bibliothek) (accessed on June 1st, 2020).

It containes more than 100 000 annotated poems from over 200 authors.

## Statistics

- Authors: 227
- Works: 105849
- Stanzas: 515664
- Verses: 3422223
- Words: 20735344
- Characters: 120830774

The file [`textgrid-poetry.json`](./textgrid-poetry.json) contains the corpus. The format of each entry is as follows:

```json
{
    "author": "Schwab, Gustav",
    "authorRef": "pnd:118762745",
    "publicationDate": "1880",
    "title": "6. [Und vor mein schlummernd Auge trat ein Knabe]",
    "text": [
        [
            "Und vor mein schlummernd Auge trat ein Knabe,",
            "Leichtsinn'gen Schritts, gleichg\u00fcltigen Gesichts;",
            "In seinem Blick, um seinen Mund war nichts;",
            "Der deutete hinaus mit seinem Stabe"
        ],
        ...
    ]
},
```

Folder [`json`](./json) contains the works by author.

The script [`textgrid-poetry.py`](./textgrid-poetry.py) was used to download and extract all the data.

```bash
$ ./textgrid-poetry.py --help
usage: Generates a JSON corpus from the poetry part of TextGrid (https://textgrid.de/en/digitale-bibliothek)
       [-h] [-d] [-np] [--json-folder JSON_FOLDER] [--corpus-file CORPUS_FILE]
       [files [files ...]]

positional arguments:
  files                 Zip file names containing the corpus ('literatur-nur-
                        texte-1.zip', 'literatur-nur-texte-2.zip')

optional arguments:
  -h, --help            show this help message and exit
  -d, --download        Download the zip files containing the corpus
                        ('https://textgrid.de/fileadmin/digitale-
                        bibliothek/literatur-nur-texte-1.zip',
                        'https://textgrid.de/fileadmin/digitale-
                        bibliothek/literatur-nur-texte-2.zip')
  -np, --no-parse       Parse the content of the zip files
  --json-folder JSON_FOLDER
                        path to parsed json content. Defaults to './json'
  --corpus-file CORPUS_FILE
                        path to generated json corpus. Defaults to
                        './textgrid-poetry.json'
```

## License

**Verbatim from https://textgrid.de/en/digitale-bibliothek.**

```
Licensing

Since a publishing company (Editura, operator of zeno.org) digitised texts in the public domain and provided the XML mark up, the company owns the ancillary copyright to the digitised, compiled and marked texts. TextGrid acquired the licence to use this digitised and XML-marked collection of texts on the condition that Editura is mentioned (Creative Commons licence “by” version 3.0).
In order to relay the annotated data stock including the metadata with as few restrictions as possible, TextGrid will also make this data stock available under the Creative Commons licence “by” version 3.0.
The texts as such, i.e. the texts without annotations and without added metadata, are available in the public domain. Texts already in the public domain are not affected by licensing.
TextGrid created a new database by processing and structuring the texts as well as editing the metadata; this database is automatically subject to own ancillary copyrights in accordance with general copyright regulations. These copyrights are also regulated by the Creative Commons licence “by” version 3.0.
Hence, the data stock of the Digital Library can be:

- reproduced, distributed and made available to the general public
- used to adapt and edit the content
- used commercially

Refer to: http://creativecommons.org/licenses/by/3.0/
In each case, TextGrid must be mentioned in the form: TextGrid.
Should you pass on data of the data stock that are protected, please add the following information:The work title by name is a modification of the data stock of TextGrid’s Digital Library, www.editura.de, and is published under the Creative Commons licence.
```
