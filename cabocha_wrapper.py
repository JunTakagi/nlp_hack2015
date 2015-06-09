#!/usr/bin/python
# -*- coding: utf-8 -*-

import CaboCha

sentence = "その赤い猫は、黒猫のしっぽを噛み、逃げた"


class TokenSequence:
  surface = None
  feature = None

class Token:
  surface = None
  feature = None
  def __init__(self, token):
    self.surface = token.surface
    self.feature = token.feature.split(",")
  def dump(self, indent=""):
    print indent, self.surface, "\t", ",".join(self.feature)

class Chunk:
  surface = None
  refTo = None
  refFrom = None
  tokens = None
  func = None
  head = None
  score = None
  def __init__(self, cabo_chunk):
    self.surface = None
    self.refTo = None
    self.refFrom = []
    self.tokens = None
    self.head = None
    self.func = None
    self.score = 0.0
  def dumpSelf(self, indent=""):
    print indent, "== chunk =="
    print indent, "\tHead:",
    self.head.dump()
    print indent, "\tFunc:",
    self.func.dump()
    for t in self.tokens:
      print indent, "\t",
      t.dump()
  def dumpAll(self, indent=""):
    self.dumpSelf(indent)
    print
    postIndent = indent + "\t"
    for c in self.refFrom:
      c.dumpAll(postIndent)

class SentenceTree:
  chunks = None
  tokenSeqences = None
  tokens = None
  def __init__(self, tree):
    self.chunks = [None] * tree.chunk_size()
    self.tokens = [None] * tree.token_size()
    for t in range(tree.token_size()):
      self.tokens[t] = Token(tree.token(t))
    for i in reversed(range(tree.chunk_size())):
      cabo_chunk = tree.chunk(i)
      chunk = Chunk(cabo_chunk)
      link = cabo_chunk.link
      if link != -1:
        chunk.refTo = self.chunks[link]
        self.chunks[link].refFrom.append(chunk)
      chunk.tokens = self.tokens[cabo_chunk.token_pos:cabo_chunk.token_pos+cabo_chunk.token_size]
      chunk.head = self.tokens[cabo_chunk.token_pos+cabo_chunk.head_pos]
      chunk.func = self.tokens[cabo_chunk.token_pos+cabo_chunk.func_pos]
      self.chunks[i] = chunk
  def dump(self):
    self.chunks[len(self.chunks)-1].dumpAll()

# c = CaboCha.Parser("");
class CaboChaWrapper:
  parser = None
  def __init__(self, option=""):
    self.parser = CaboCha.Parser(option)
  def parse(self, sentence):
    tree = self.parser.parse(sentence)
    return SentenceTree(tree)

if __name__ == "__main__":
  import sys
  c = CaboChaWrapper()
  c.parse(sys.argv[1]).dump()
