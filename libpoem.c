/* Compile with gcc -shared -o libpoem.so libpoem.c */
#include <stdio.h>

int this_is_an_external_func_in_a_lib() {
	puts("ARM disassembly");          //5
	puts("Reading symbol resolving"); //7
	puts("In the cold of night");     //5
	return 42;
}
