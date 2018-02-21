/* gcc -o proj -Wl,-rpath=. -L. -I. -l poem proj.c */
#include "libpoem.h"

int main() {
	int ret;
	ret=this_is_an_external_func_in_a_lib();
	return ret;
}
