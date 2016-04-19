#!/usr/bin/python3
from bs4 import BeautifulSoup
from inspect import currentframe
from itertools import chain
from os import path
from os.path import dirname
from subprocess import run
from tempfile import NamedTemporaryFile
from urllib.parse import urlencode, urljoin
from urllib.request import urlopen

import click

@click.group()
def cli():
  pass

CAMPUSOnline = 'https://online.tugraz.at/tug_online/'

@cli.command()
@click.argument('term')
def search_employee(term):
  """Search for employees of TU Graz."""
  url = urljoin(CAMPUSOnline, 'wbSuche.bedienstetenSuche')
  post_data = urlencode({'pSuchbegriff': term}).encode('utf-8')
  with urlopen(url, post_data) as response:
    content = str(BeautifulSoup(response, 'lxml'))
    # Remove DOCTYPE (which chokes XQilla XML parser)
    content = remove_first_line(content)
    with NamedTemporaryFile(mode='w') as xml:
      print(content, file=xml)
      xml.flush()
      xqilla(function_name(), xml.name)

@cli.command()
@click.argument('term')
def coins_and_precious_metals(term):
  """Display current pricing of Erste Group coins and precious metals."""
  with urlopen('https://produkte.erstegroup.com/Retail/de/MarketsAndTrends/Currencies/Sites/EB_Fixings_and_Downloads/Coins_and_Precious_Metals/index.phtml') as response:
    soup = BeautifulSoup(response, 'lxml')
    with NamedTemporaryFile(mode='w') as xml:
      print('<html><body>', file=xml)
      for table in soup.find_all('table'): print(table.prettify(), file=xml)
      print('</body></html>', file=xml)
      xml.flush()
      xqilla(function_name(), xml.name, variables={'query': term})

###############################################################################

def function_name():
  return currentframe().f_back.f_code.co_name
    
def remove_first_line(content):
  return content[content.find('\n')+1:-1]

def xq(basename):
  return path.abspath(path.join(dirname(__file__), basename + ".xq"))

def xqilla(xq_base, context=None, variables={}):
  cmd = ['xqilla']
  if context is not None: cmd.extend(['-i', context])
  cmd.extend(chain.from_iterable((['-v', k, v] for k, v in variables.items())))
  cmd.append(xq(xq_base))
  run(cmd, check=True)

if __name__ == '__main__':
  cli()
