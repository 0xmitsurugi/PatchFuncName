# PatchFuncName

Warning, this is highly experimental code. for the moment, it can patch function name in the proj and libpoem.so.

You can use the _patch.py_ program to do so. You can use any string with 33 characters, with any characters except the \x00. There is hardcoded offsets in the file, so don't expect it to work anywhere than the libpoem.so provided. It should be easy to modify it to work for any file, though. proj and libpoem.so are compiled for a raspberrypi.

The _hashparse.py_ can parse the .gnu.hash section of ELF files, it should work anywhere.
The dl\_new\_hash.py can calculate hashes.

Those files have been used to create the blogpost: http://0x90909090.blogspot.fr/2018/02/fun-with-function-names-where-resolving.html

