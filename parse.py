import os
import argparse
from bs4 import BeautifulSoup
import jinja2


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
