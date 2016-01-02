from os import path, listdir
from hashlib import sha512, sha256, md5
from base64 import b64encode
import re

JS_DIR = path.normpath(path.join(__file__, "..", ".."))

'''
Yield each file in the javascript directory
'''
def js_files():
  for f in listdir(JS_DIR):
    if path.isfile(f) and f.endswith(".js"):
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
  for file in js_files():
    print "Generating content for {0!s}".format(file)
    base = path.splitext(path.basename(file))[0]
    var_name = re.sub(r"[^a-z0-9]", "_", base)
    content = "{0!s}=true;".format(var_name)
    with open(file, "w") as f: f.write(content)
    print "\tSHA512 integrity: {0!s}".format(sha512_uri(content))
    print "\tSHA256 integrity: {0!s}".format(sha256_uri(content))
    print "\tMD5 integrity:    {0!s}".format(md5_uri(content))

if __name__ == "__main__":
  main()
