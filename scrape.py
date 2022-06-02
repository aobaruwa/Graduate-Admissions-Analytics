import requests
from tqdm import trange

url_form = "https://www.thegradcafe.com/survey/?institution=&program=&degree=&season=&page={}&per_page=40"
DATA_DIR = './data/'

if __name__ == '__main__':
  for i in trange(1, 998):
    url = url_form.format(i)
    r = requests.get(url)
    r.encoding = 'utf-8'
    fname = "{data_dir}/{page}.html".format(data_dir=DATA_DIR, page=str(i))
    with open(fname, 'w') as f:
      f.write(r.text)
      
