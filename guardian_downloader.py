import json
import requests
import pdb
from os import makedirs
from os.path import join, exists
from datetime import date, timedelta

OUTPUT_DIR = join('tmp', 'raw')
makedirs(OUTPUT_DIR, exist_ok=True)
# Sample URL
#
# http://content.guardianapis.com/search?from-date=2016-01-02&
# to-date=2016-01-02&order-by=newest&show-fields=all&page-size=200
# &api-key=your-api-key-goes-here

MY_API_KEY = open("creds_guardian.txt").read().strip()
API_ENDPOINT = 'http://content.guardianapis.com/search'
my_params = {
  'order-by': "newest",
  'show-fields': 'all',
  'type': 'article',
  'show-tags': 'contributor',
  'page-size': 200,
  'api-key': MY_API_KEY
}


# day iteration from here:
# http://stackoverflow.com/questions/7274267/print-all-day-dates-between-two-dates
start_date = date(2016, 5, 1)
end_date = date(2016, 5, 30)
dayrange = range((end_date - start_date).days + 1)
for daycount in dayrange:
  dt = start_date + timedelta(days=daycount)
  datestr = dt.strftime('%Y-%m-%d')
  fname = join(OUTPUT_DIR, datestr + '.json')
  if not exists(fname):
    # then let's download it
    print("Downloading", datestr)
    all_results = []
    my_params['from-date'] = datestr
    my_params['to-date'] = datestr
    current_page = 1
    total_pages = 1
    while current_page <= total_pages:
      print("...page", current_page)
      my_params['page'] = current_page
      resp = requests.get(API_ENDPOINT, my_params)
      data = resp.json()
      all_results.extend(data['response']['results'])
      # if there is more than one page
      current_page += 1
      total_pages = data['response']['pages']

    with open(fname, 'w') as f:
      print("Writing to", fname)

      # re-serialize it for pretty indentation
      f.write(json.dumps(all_results, indent=2))
