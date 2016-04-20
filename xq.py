#!/usr/bin/python3
from bs4 import BeautifulSoup
from bs4.element import Doctype, ResultSet
from inspect import currentframe
from itertools import chain
from os import path
from os.path import abspath, dirname
from subprocess import PIPE, run
from tempfile import NamedTemporaryFile
from urllib.parse import urljoin

import click
import requests

@click.group()
def cli():
  pass

@cli.command()
@click.argument('term')
def search_employee(term):
  """Search for employees of TU Graz."""
  CAMPUSOnline = 'https://online.tugraz.at/tug_online/'
  scrape(post=urljoin(CAMPUSOnline, 'wbSuche.bedienstetenSuche'),
         data={'pSuchbegriff': term})

@cli.command()
@click.argument('term')
def coins_and_precious_metals(term):
  """Display current pricing of Erste Group coins and precious metals."""
  scrape(get='https://produkte.erstegroup.com/Retail/de/MarketsAndTrends/Currencies/Sites/EB_Fixings_and_Downloads/Coins_and_Precious_Metals/index.phtml',
         find_all='table',
         xquery_vars={'query': term})

@cli.command()
@click.argument('language')
@click.argument('query')
def github_code_search(language, query):
  """Search for source code on GitHub."""
  scrape(get='https://github.com/search',
         params={'l': language, 'q': query, 'type': 'code'})

###############################################################################

def scrape(get=None, post=None, find_all=None,
           xquery_name=None, xquery_vars={}, **kwargs):
  response = None
  url = None
  context = None

  if get is not None:
    response = requests.get(get, **kwargs)
  elif post is not None:
    response = requests.post(post, **kwargs)

  if response is not None:
    response.raise_for_status()
    context = BeautifulSoup(response.text, 'lxml')
    dtd = next(context.descendants)
    if type(dtd) is Doctype:
      dtd.extract()
    if find_all is not None:
      context = context.find_all(find_all)
    url = response.url

  if xquery_name is None:
    xquery_name = currentframe().f_back.f_code.co_name
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
  cmd.extend(chain.from_iterable(['-v', k, v] for k, v in xquery_vars.items()))
  if url is not None:
    cmd.extend(['-b', url])
  cmd.append(abspath(path.join(dirname(__file__), xquery_name + ".xq")))

  output = run(cmd, stdout=PIPE, check=True).stdout.decode('utf-8')
  if type(context) is NamedTemporaryFile: context.close()

  print(output, end='')

if __name__ == '__main__':
  cli()
