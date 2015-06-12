#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import bs4
import re

HEAD_STRIP = re.compile(u"^(\s)+")

SKIP = ['br', '', None]

class AOZORA:
  scenes = []
  ruby_scenes = []
  surface = ""
  ruby = ""
  def __init__(self):
    self.scenes = []
    self.ruby_scenes = []
    self.surface = ""
    self.ruby = ""
  def add(self, uni):
    if uni != u"\n" or self.surface != u"": # new line at the top of scene
      self.surface += uni
      self.ruby += uni
  def addSurface(self, uni):
    self.surface += uni
  def addRuby(self, uni):
    self.ruby += uni
  def changeScene(self):
    if self.surface != u"":
      self.scenes.append(self.surface.rstrip())
      self.ruby_scenes.append(self.ruby.rstrip())
      self.surface = u""
      self.ruby = u""
  def getSurface(self):
    ret = u""
    for scene in self.scenes:
      ret += scene
    return ret
  def getRuby(self):
    ret = u""
    for scene in self.ruby_scenes:
      ret += scene
    return ret
  def EOL(self):
    if self.scenes == [] or self.scenes[len(self.scenes)-1] != self.surface:
      self.changeScene()
  def dump(self):
    count = 0
    for scene in self.scenes:
      print "==================", count, "=================="
      print scene.encode('utf-8')
      count += 1
    count = 0
    for scene in self.ruby_scenes:
      print "==================", count, "=================="
      print scene.encode('utf-8')
      count += 1

def clean_unicode(uni):
  ret = uni.strip()
  return ret

def create_novel_data(data):
  ret = AOZORA()
  dump_tag(data, ret)
  ret.EOL()
  return ret

def dump_tag(tag, result):
  if tag == None:
    return
  elif isinstance(tag, bs4.element.NavigableString):
    ret = clean_unicode(unicode(tag))
    result.add(ret)
  elif tag.name == 'br':
    result.add(u"\n")
  elif tag.name == 'a' and 'class' in tag.attrs.keys() and 'midashi_anchor' in tag['class']: # seen change
    result.changeScene()
  elif tag.name == 'ruby':
    rb = tag.find('rb')
    rt = tag.find('rt')
    surface = create_novel_data(rb)
    ruby = create_novel_data(rt)
    result.addSurface(surface.getSurface())
    result.addRuby(ruby.getRuby())
  else:
    children = tag.children
    if children != None:
      for child in children:
        dump_tag(child, result)

soup = BeautifulSoup(open('docs/kusamakura.xml', 'r'))

divs = soup.body.find_all('div')
main_text = None
for div in divs:
  if div != None and 'class' in div.attrs.keys() and "main_text" in div['class']:
    main_text = div
    break

result = AOZORA()

dump_tag(main_text, result)
result.dump()
#surface, ruby = dump_tag(main_text)
for scene in result.scenes:
  print scene.encode('utf-8')
