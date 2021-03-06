from os import path, listdir
from hashlib import sha512, sha384, sha256, md5
from base64 import b64encode
import re

DIR = path.normpath(path.join(__file__, "..", ".."))

'''
Yield each javascript and css file in the directory
'''
def js_and_css_files():
  for f in listdir(DIR):
    if path.isfile(f) and (f.endswith(".js") or f.endswith(".css")):
      yield f

'''
URL-safe base64 encode a binary digest and strip any padding.
'''
def format_digest(digest):
  return b64encode(digest)

'''
Generate an encoded sha512 URI.
'''
def sha512_uri(content):
  return "sha512-{0!s}".format(format_digest(sha512(content).digest()))

'''
Generate an encoded sha384 URI.
'''
def sha384_uri(content):
  return "sha384-{0!s}".format(format_digest(sha384(content).digest()))

'''
Generate an encoded sha256 URI.
'''
def sha256_uri(content):
  return "sha256-{0!s}".format(format_digest(sha256(content).digest()))

'''
Generate an encoded md5 digest URI.
'''
def md5_uri(content):
  return "md5-{0!s}".format(format_digest(md5(content).digest()))

def main():
  for file in js_and_css_files():
    print "Listing hash values for {0!s}".format(file)
    with open(file, "r") as content_file:
      content = content_file.read()
      print "\tSHA512 integrity: {0!s}".format(sha512_uri(content))
      print "\tSHA384 integrity: {0!s}".format(sha384_uri(content))
      print "\tSHA256 integrity: {0!s}".format(sha256_uri(content))
      print "\tMD5 integrity:    {0!s}".format(md5_uri(content))

if __name__ == "__main__":
  main()
