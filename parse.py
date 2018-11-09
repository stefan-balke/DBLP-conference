import os
import argparse
from bs4 import BeautifulSoup
import jinja2
import simplejson as json
import string
from nameparser import HumanName
import unicodedata


def get_dblp_key(authors, year):

    if isinstance(authors, str):
        authors = [authors]

    # start with first author's full name
    key = HumanName(authors[0]).last
    key = key.capitalize()  # e.g. de Val
    key = key.replace(' ', '')
    key = key.replace('ß', 'ss')
    key = key.replace('ä', 'ae')
    key = key.replace('ö', 'oe')
    key = key.replace('ü', 'ue')

    # append co-authors' first letter from name
    for au in authors[1:]:
        cur_author = HumanName(au)
        key += cur_author.last[0]

    # add year
    key += str(year)[2:]

    key = unicodedata.normalize('NFKD', key).encode('ascii', 'ignore').decode()

    return str(key)


def check_key(key, keys):
    if cur_json_key in json_output.keys():
        print('double key {}'.format(cur_json_key))
        return True
    else:
        return


def parse_input(html):
    """Parse HTML input file.
    This parser is specific to the ISMIR 2017 electronic proceedings.
    """
    # parse input file
    soup = BeautifulSoup(html_doc, 'html.parser')

    entries = []

    for cur_row in soup.find_all('tr'):
        cur_entry = {}
        cur_entry['title'] = cur_row.find('a').contents[0]
        cur_entry['authors'] = cur_row.find('em').contents[0].replace(',', ' and')
        cur_entry['url'] = cur_row.find('a')['href']

        entries.append(cur_entry)

    return entries


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DBLP conference tool.')
    parser.add_argument('--input', type=str, help='path to the input file')
    args = parser.parse_args()

    # open input file
    with open(args.input) as f:
        html_doc = f.read()

    entries = parse_input(html_doc)

    # load jinja template
    PATH = os.path.dirname(os.path.abspath(__file__))
    template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(PATH, 'templates')))
    template = template_env.get_template('template_dblp.txt')

    # render template and write output to file
    with open('output.txt', 'w') as f:
        html = template.render({'entries': entries})
        f.write(html)

    # create json output
    json_output = dict()
    CONF_YEAR = 2018

    for cur_entry in entries:

        cur_authors = cur_entry['authors'].split(' and ')
        cur_dblp_key = get_dblp_key(cur_authors, CONF_YEAR)
        cur_json_key = 'conf/ismir/' + cur_dblp_key

        cur_entry_json = dict()
        cur_entry_json['@key'] = cur_json_key
        cur_entry_json['@mdate'] = ''
        cur_entry_json['author'] = cur_authors
        cur_entry_json['title'] = cur_entry['title']
        cur_entry_json['year'] = CONF_YEAR
        cur_entry_json['crossref'] = 'conf/ismir/' + str(CONF_YEAR)
        cur_entry_json['booktitle'] = 'ISMIR'
        cur_entry_json['url'] = ''
        cur_entry_json['ee'] = 'http://ismir2018.ircam.fr/doc/' + cur_entry['url'].replace('articles', 'pdfs')
        cur_entry_json['record_id'] = ''
        cur_entry_json['doi'] = ''

        # check if key is unique
        cur_key = cur_json_key
        cur_char_idx = 0

        while (cur_key in json_output.keys()):
            # add small character to key to make unique
            cur_key = cur_json_key + string.ascii_lowercase[cur_char_idx]

        # just double-checking key uniqueness
        if cur_key in json_output.keys():
            raise('double key {}'.format(cur_json_key))

        json_output[cur_key] = cur_entry_json

    with open('output.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_output, indent=2))
