#!/usr/bin/env python

import io
import sys
import to_uri
import re
import time

def readfile(fn):
    with io.open(fn, 'Ur', encoding='utf8') as f:
        return f.read()
def loaderString(var):
    fn = var.group(1)
    if fn.find('.js')>=0:
      fn1=replaceFile(fn)
    else:
      if fn.find('.css')>=0:
        fn1=replaceFile(fn)
      else:
        fn1=readFile(fn)
    return fn1.replace('\n', '\\n').replace('\'', '\\\'')

def loaderRaw(var):
    fn = var.group(1)
    return replaceFile(fn)

def loaderFile(var):
    fn = var.group(1)
    if fn.find('.js')>=0:
      fn1=replaceFile(fn)
    else:
      if fn.find('.css')>=0:
        fn1=replaceFile(fn)
      else:
        fn1=to_uri.img_to_data(fn)
    return fn1

def replaceFile(var):
  print var
  m = readfile(var)
  m = m.replace('@@BUILDDATE@@', n)
  m = re.sub('@@INCLUDERAW:([0-9a-zA-Z_./-]+)@@', loaderRaw, m)
  m = re.sub('@@INCLUDESTRING:([0-9a-zA-Z_./-]+)@@', loaderString, m)
  m = re.sub('@@INCLUDEURI:([0-9a-zA-Z_./-]+)@@', loaderFile, m)
  return(m)


def build_file(path):
	n = time.strftime('%Y-%m-%d-%H%M%S')
	m = readfile(path)
	m = m.replace('@@BUILDDATE@@', n)
	m = re.sub('@@INCLUDERAW:([0-9a-zA-Z_./-]+)@@', loaderRaw, m)
	m = re.sub('@@INCLUDESTRING:([0-9a-zA-Z_./-]+)@@', loaderString, m)
	m = re.sub('@@INCLUDEURI:([0-9a-zA-Z./-]+)@@', loaderFile, m)
	with io.open('debug.'+path, 'w', encoding='utf8') as f:
	    f.write(m)

if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit(1)
    print build_file(path)

