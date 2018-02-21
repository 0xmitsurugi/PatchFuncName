#! /usr/bin/python

#This is propa codaz

#Will rewrite it someday. perhaps. "It works for me (c)"
#For the moment, it only works with libpoem.so because of hardcoded offsets.

import sys
import os
import struct

old_func="this_is_an_external_func_in_a_lib"
len_func=len(old_func)
old_lib="libpoem.so.ori"
old_proj="proj.ori"
new_lib="libpoem.so"
new_proj="proj"

if len(sys.argv) == 2:
    if len(sys.argv[1]) == 33:
        chaine = sys.argv[1]
    elif len(sys.argv[1]) > 10 and len(sys.argv[1]) != 33:
        chaine = sys.argv[1]
        if len(chaine)%2 != 0:
            print "give input in hex"
            exit(1)
        l=len(chaine)
        print "we have %d char, must add %d to get 33" % (l/2,33-l/2)
        chaine = chaine + '41'*(33-(l/2))
        chaine=chaine.decode('hex')
    else:
        print "Give a longer chaine"
        exit(1)
else:
    print "Give a new name"
    exit(1)


def dl_new_hash(func):
    h=5381
    for c in list(func):
        h=h*33+ord(c)
    h=hex(h & 0xffffffff)[2:-1]
    print "  [+] hash results for %s is 0x%s" % (func,h.upper())
    return h[6:8]+h[4:6]+h[2:4]+h[0:2]



print "[+] Patching func with name (in hex): %s\n" % chaine.encode('hex')

##Get buckets number
result=os.popen("readelf -S "+old_lib+" | grep .gnu.hash | awk '{ print $5,$6,$7; }'").readlines()
if len(result)==1:
    print "[+] Ok, one line. Good"
else:
    print "[ ] Problem with readelf, quitting here"
    exit(1)
result=result[0].rstrip()
start,offset,size=result.split(' ')
start=int(start,16)

f=open(old_lib,"rb")
data=f.read(start+4)[start:start+4]
f.close()
nbuckets=struct.unpack("<I",data)
print "[+] nbuckets is %d" % nbuckets
nbuckets=nbuckets[0]

a=int(dl_new_hash(old_func),16)
b=int(dl_new_hash(chaine),16)
if (a % nbuckets) == (b % nbuckets):
    print "    Guess: Working"
else:
    print "    Guess: Broken"
    exit(1)


print "[+] Patching proj binary"
f=open(old_proj,"rb")
data=f.read()
f.close()

#Beware of string findings
new_data=data.replace(old_func,chaine)

f=open(new_proj,"wb")
f.write(new_data)
f.close()

print "[+] Opening %s" % old_lib
f=open(old_lib,"rb")
data=f.read()
f.close()

#This is hardcoded. You can change them.
#Or write a function findings those offsets.
#offsets list
ofbloom1=0x128
ofbloom2=0x12c
ofh=0x144
of1=0x2e5
of2=0x1795

print "  [+] Patching bloom filter"
new_data=data[0:ofbloom1]+"\xff\xff\xff\xff"+data[ofbloom1+4:ofbloom2]+"\xff\xff\xff\xff"
print "  [+] Patching hash"
new_data=new_data+data[ofbloom2+4:ofh]+dl_new_hash(chaine).zfill(8).decode('hex')
print "  [+] Patching function name"
new_data=new_data+data[ofh+4:of1]+chaine+data[of1+len_func:of2]+chaine+data[of2+len_func:]
f=open(new_lib,"wb")
f.write(new_data)
f.close()
