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
  INPUT_DIR = join('tmp', 'raw')
  OUTPUT_DIR = join('tmp', 'parsed')
  makedirs(OUTPUT_DIR, exist_ok=True)

  count = 0
  previous_date = ''
  for fname in os.listdir(INPUT_DIR):
    print("Parsing", fname)
    with open(join(INPUT_DIR, fname), 'r') as f:
      data = json.load(f)
      for d in data:
        d_new = {}
        # add data
        for field_name in ['id', 'sectionId', 'webTitle', 'webPublicationDate', 'webUrl', 'apiUrl']:
          d_new[field_name] = d[field_name]

        d_new['guardianId'] = d_new['id']
        date = d_new['webPublicationDate'].split('T', 1)[0]

        if date != previous_date:
          count = 1
        else:
          count = count + 1

        previous_date = date

        d_new['id'] = date + '-' + str(count)
        d_new['body'] = parse_tags(d['fields']['body']).strip()

        # parse contributor
        d_new['authors'] = []
        d_new['keyword'] = []
        for tag in d['tags']:
          tag_new = {}
          if tag['type'] == 'contributor':
            tag_new['id'] = tag['id']
            tag_new['webTitle'] = tag['webTitle']
            d_new['authors'].append(tag_new)
          if tag['type'] == 'keyword':
            tag_new['id'] = tag['id']
            tag_new['webTitle'] = tag['webTitle']
            try:
              tag_new['sectionId'] = tag['sectionId']
              tag_new['sectionName'] = tag['sectionName']
            except:
              pass
            d_new['keyword'].append(tag_new)


        result_fname = join(OUTPUT_DIR, d_new['id'] + '.json')
        with open(result_fname, 'w') as f:
          print("Writing to", result_fname)

          # re-serialize it for pretty indentation
          f.write(json.dumps(d_new, indent=2))

if __name__ == "__main__":
  main()
