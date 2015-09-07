#!/usr/bin/python3
"""
TO WRITE
"""

from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader
import os
import re
import sys


def parse_dico_file(dicofile):
    """
    Parse telemac dictionary file (for one module)
    Return a list of keywords as a dict type
    """
    def remove_surrounding_char(string, char):
        """Return a string without surrounding char if present"""
        if string.startswith(char) and string.endswith(char):
            return string[1:-1]
        else:
            return string

    def iter_on_keyword():
        """
        Generate an iterator on each keyword of dicofile
        keyword is a dict with key from variable `keys`
        """
        with open(dicofile, 'r', encoding='iso-8859-1') as filein:
            content = filein.readlines()
            last_key = None
            keyword = {}

            for line in content:
                line = line.strip()  # remove trailing whitespaces and line breaking
                line = line.replace("''", "'")  # for French apostrophe
                key_found = False

                if not line.startswith('/') and line != '':
                    for key in keys:
                        # Find if current line starts with a key
                        if re.search('{}\s*='.format(key), line):
                            if key == FIRST_KEY and last_key is not None:
                                # A new keyword is reached...

                                for key2clean, value in keyword.items():
                                    # Remove surrounding quotation mark (and trailing space)"
                                    # Not possible do it before because values are build by concatenation
                                    keyword[key2clean] = remove_surrounding_char(keyword[key2clean], "'").strip()

                                yield keyword
                                # Clean for next keyword
                                keyword = {}

                            value = line.split('=')[1]
                            keyword[key] = value.strip()
                            last_key = key
                            key_found = True
                            break

                    if not key_found and last_key is not None:
                        # The current key is written on multiple lines
                        keyword[last_key] = keyword[last_key] + '\n' + line

    # Build keywords by step
    keywords = []
    for keyword in iter_on_keyword():
        keywords.append(keyword)

    return keywords

# ~> VARIABLES TO PARSE DICO FILES
# Telemac dico files (one per module) consists of list of keywords.
# A keyword has several keys with a corresponding value.
# The keys are precised in a variable, and the value correspond to the text
#   after the = symbol and can be written on multiple lines
FIRST_KEY = 'NOM'  # recognize a new keyword (first key in the block of keys)
keys = ['NOM', 'NOM1', 'TYPE', 'INDEX', 'MNEMO', 'TAILLE', 'SUBMIT', 'DEFAUT', 'DEFAUT1', 'CHOIX', 'CHOIX1', 'RUBRIQUE', 'RUBRIQUE1', 'COMPORT', 'NIVEAU', 'APPARENCE', 'AIDE', 'AIDE1']  # some are optional (order is not relevant)

# ~> VARIABLE TO WRITE DEFINITION FILES
# Keys to find keyword name
name = {'fr': 'NOM',
        'en': 'NOM1'}

# Keys to write in definition files
labels2write = {
    'fr': OrderedDict({
        'DEFAUT': 'DÉFAUT',
        'CHOIX': 'CHOIX',
        'AIDE': 'AIDE'
    }),
    'en': OrderedDict({
        'DEFAUT1': 'DEFAULT',
        'CHOIX1': 'CHOICE',
        'AIDE1': 'HELP'
    })}

if __name__ == "__main__":
    # ~> SELECT MODULES AND LANGUAGE TO EXPORT
    lang = 'fr'
    modules = ['artemis', 'postel3d', 'sisyphe', 'stbtel', 'telemac2d', 'telemac3d', 'tomawac']

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('renderer.xhtml')

    def outfile(module):
        return module + '.xhtml'

    links = [(module, outfile(module)) for module in modules]

    for module in modules:
        dicofile = os.path.join('dico', '{}.dico'.format(module))
        print("~> Module {} (language(s) = {})".format(module, lang))
        keywords = parse_dico_file(dicofile)

        keywords.sort(key=lambda x: x[name[lang]])

        keywords2write = []

        for keyword in keywords:
            cur_keyword = OrderedDict()
            for key, label in labels2write[lang].items():
                if key in keyword.keys():
                    text = keyword[key].replace('\n', '<br />').replace('&', '&amp;')  #FIXME html chars and tags
                    cur_keyword[label] = text
            keywords2write.append((keyword[name[lang]], cur_keyword))

        with open(outfile(module), 'w') as fileout:
            fileout.write(template.render(
                module=module,
                links=links,
                keywords=keywords2write,
            ))

    print('My work is done...')
