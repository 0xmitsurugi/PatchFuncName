#! /usr/bin/python

import sys
if len(sys.argv) !=2:
    print "Give a name"
    print "Bye.."

if len(sys.argv) == 2:
    print "[+] Calculating hash for %s" % sys.argv[1]
    func=sys.argv[1]
else:
    func='\x0d\x0aA\x0d\x0a'

h=5381
for c in list(func):
    h=h*33+ord(c)


hash=hex(h & 0xffffffff)[2:-1].upper()

print "Output is 0x%s" % hash
#print "Output2 is 0x%s" % hex(h)[2:-1].upper()
