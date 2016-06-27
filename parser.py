from html.parser import HTMLParser
from os import makedirs
from os.path import join, exists
import os
import json

class TextParser(HTMLParser):
  def __init__(self):
    self.reset()
    self.strict = False
    self.convert_charrefs= True
    self.fed = []

  def handle_data(self, d):
    self.fed.append(d)

  def get_data(self):
    return ''.join(self.fed)

def parse_tags(html):
  s = TextParser()
  s.feed(html)
  return s.get_data()

def main():
  RAW_DIR = join('tmp', 'raw')
  RESULT_DIR = join('tmp', 'parsed')
  makedirs(RESULT_DIR, exist_ok=True)

  for fname in os.listdir(RAW_DIR):
    print("Parsing", fname)
    result_data = []
    with open(join(RAW_DIR, fname), 'r') as f:
      data = json.load(f)
      for d in data:
        d_new = {}
        # add data
        for field_name in ['id', 'sectionId', 'webTitle', 'webPublicationDate', 'webUrl', 'apiUrl']:
          d_new[field_name] = d[field_name]

        d_new['body'] = parse_tags(d['fields']['body'])

        # parse contributor
        d_new['authors'] = []
        for a in d['tags']:
          a_new = {}
          a_new['id'] = a['id']
          a_new['webTitle'] = a['webTitle']

          d_new['authors'].append(a_new)

        result_data.append(d_new)

    result_fname = join(RESULT_DIR, fname)
    with open(result_fname, 'w') as f:
      print("Writing to", result_fname)

      # re-serialize it for pretty indentation
      f.write(json.dumps(result_data, indent=2))

if __name__ == "__main__":
  main()