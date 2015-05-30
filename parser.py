#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re


def parse(filename):
  paragraphes = []
  speeches = []
  sentences = []
  start = re.compile('^-+$')
  count = 0
  fd = open(filename, 'r')
  for line in fd:
    line = line.rstrip()
    line = line.decode('shift-jis')
    if start.match(line):
      count += 1
    if count >= 2:
      break
  shikiri = re.compile(u'｜')
  rubi = re.compile(u'《.+?》')
  tyushaku = re.compile(u'［.+］')
  serihu = re.compile(u'^「(.+)」$')
  serihu_end = re.compile(u'」')
  touten = re.compile(u'。')
  space = re.compile('^\s*$')
  jiage = re.compile(u'^(　|\s)+')
  for line in fd:
    line = line.rstrip()
    line = line.decode('shift-jis')
    if line == '':
      if len(sentences) != 0:
        paragraphes.append(sentences)
        sentences = []
      continue
    if tyushaku.match(line):
      continue
    # pre process
    line = re.sub(shikiri, '', line)
    line = re.sub(rubi, '', line)
    line = re.sub(tyushaku, '', line)
    line = re.sub(jiage, '', line)
    line = re.sub(serihu_end, u'」。', line)
    danraku = touten.split(line)
    for bun in danraku:
      if space.match(bun):
        continue
      if serihu.match(bun):
        speeches.append((len(paragraphes), len(sentences)))
      sentences.append(bun)
  return paragraphes, speeches

if __name__ == "__main__":
  para, spe = parse('./docs/kusamakura.txt')
  for p in para:
    print '=PARA='
    for line in p:
      print line.encode('utf-8')
  print '==SPEECH=='
  for s in spe:
    print s, para[s[0]][s[1]].encode('utf-8')