#!/usr/bin/python3
from bs4 import BeautifulSoup
from bs4.element import Doctype, ResultSet
from inspect import currentframe
from itertools import chain
from os import path
from os.path import abspath, dirname
from requests import get
from subprocess import PIPE, run
from tempfile import NamedTemporaryFile
from urllib.parse import urljoin

import click

@click.group()
def cli():
  pass

@cli.command()
@click.argument('term')
def search_employee(term):
  """Search for employees of TU Graz."""
  CAMPUSOnline = 'https://online.tugraz.at/tug_online/'
  response = get(urljoin(CAMPUSOnline, 'wbSuche.bedienstetenSuche'),
                 data={'pSuchbegriff': term})
  response.raise_for_status()
  soup = BeautifulSoup(response.text, 'lxml')
  print(xquery(function_name(), drop_dtd(soup)))

@cli.command()
@click.argument('term')
def coins_and_precious_metals(term):
  """Display current pricing of Erste Group coins and precious metals."""
  response = get('https://produkte.erstegroup.com/Retail/de/MarketsAndTrends/Currencies/Sites/EB_Fixings_and_Downloads/Coins_and_Precious_Metals/index.phtml')
  response.raise_for_status()
  soup = BeautifulSoup(response.text, 'lxml')
  print(xquery(function_name(), soup.find_all('table'), variables={'query': term}))

@cli.command()
@click.argument('language')
@click.argument('query')
def github_code_search(language, query):
  response = get('https://github.com/search', params={'l': language, 'q': query, 'type': 'code'})
  response.raise_for_status()
  soup = BeautifulSoup(response.text, 'lxml')
  print(xquery(function_name(), soup))

###############################################################################

def function_name():
  return currentframe().f_back.f_code.co_name
    
def drop_dtd(soup):
  dtd = next(soup.descendants)
  if type(dtd) is Doctype:
    dtd.extract()
  return soup

def xquery(xq_base, context=None, variables={}):
  cmd = ['xqilla']
  if context is not None:
    if type(context) is BeautifulSoup:
      soup = context
      context = NamedTemporaryFile(mode='w')
      print(soup, file=context)
      cmd.extend(['-i', context.name])
    elif isinstance(context, list) or isinstance(context, ResultSet):
      tags = context
      context = NamedTemporaryFile(mode='w')
      print('<html><body>', file=context)
      for item in tags: print(item, file=context)
      print('</body></html>', file=context)
      context.flush()
      cmd.extend(['-i', context.name])
    else:
      cmd.extend(['-i', context])
  cmd.extend(chain.from_iterable(['-v', k, v] for k, v in variables.items()))
  cmd.append(abspath(path.join(dirname(__file__), xq_base + ".xq")))

  output = run(cmd, stdout=PIPE, check=True).stdout.decode('utf-8')

  if type(context) is NamedTemporaryFile:
    context.close()

  return output

if __name__ == '__main__':
  cli()
