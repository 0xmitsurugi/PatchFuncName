#! /usr/bin/python

import os,struct,sys

DEBUG=1
BIBAL="libbjr.so.ori"
#BIBAL="libc.so"
PROG="proj"

if len(sys.argv) == 2:
    BIBAL=sys.argv[1]

def _print(s):
    if DEBUG==1:
        print s

def get_gnu_hash_position(lib):
    _print("*** Get GNU HASH section for %s"%lib)
    result=os.popen("readelf -S "+lib+" | grep .gnu.hash | awk '{ print $5,$6,$7; }'").readlines()
    if len(result)==1:
        _print("[+] Ok, one line. Good")
    else:
        print "[ ] Problem with readelf. Quitting"
        exit(1)
    result=result[0].rstrip()
    start,offset,size=result.split(' ')
    if int(start,16)==int(offset,16):
        _print("[+] GNU HASH mapping fits perfectly disk and memory layout")
        _print("    starting at 0x%s" % start)
        _print("    and size is 0x%s long" % size)
    else:
        print "[ ] GNU HASH not aligned with file layout"
        print "    It can be enhanced"
        exit(1)
    return int(start,16),int(size,16)

def extract_gnu_hash(lib,start,size):
    _print("*** Extracting .gnu.hash")
    f=open(lib,"rb")
    data = f.read(start+size)[start:start+size]
    f.close()
    return data

def parse_hash(blob):
    _print("*** Parsing...")
    header=blob[0:16]
    nbuckets,symndx,maskwords,shift2=struct.unpack("<IIII",header)
    print "[+] Header"
    print "%d hash buckets" % nbuckets
    print "%d symndx" % symndx
    print "%d bloom masks" % maskwords
    print "%d bloomshift (minimum 6)" % shift2
    print "[+] Part 2 - bloom masks"
    for i in range(maskwords):
        mL=struct.unpack("<I",blob[(4+i)*4:(4+i+1)*4])
        mB=struct.unpack(">I",blob[(4+i)*4:(4+i+1)*4])
        print " Mask %d : %s \t| %s" % (i,hex(mL[0]),hex(mB[0]))
    print "[+] Part 3 - N Buckets of hash"
    cursor=4+maskwords
    for i in range(nbuckets):
        nL=struct.unpack("<I",blob[(cursor+i)*4:(cursor+i+1)*4])
        nB=struct.unpack(">I",blob[(cursor+i)*4:(cursor+i+1)*4])
        print " Bucket %d : %s \t| %s" % (i,hex(nL[0]),hex(nB[0]))
    print "[+] Part 4 - Hashes"
    cursor=(4+maskwords+nbuckets)
    end=len(blob)/4
    for i in range(cursor,end):
        hL=struct.unpack("<I",blob[(i)*4:(i+1)*4])
        hB=struct.unpack(">I",blob[(i)*4:(i+1)*4])
        print " Hash %d : %s \t| %s" % (i-cursor,hex(hL[0]),hex(hB[0]))



start,size=get_gnu_hash_position(BIBAL)
blob=extract_gnu_hash(BIBAL,start,size)
parse_hash(blob)
