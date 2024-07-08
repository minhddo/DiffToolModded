#include <stdio.h>

int main(int argc, char** argv){
		int a = 2;
		int b = 3;
		b = a + b;
		int c = a - b;
		for (int i = 0; i < 3; i++){
				a += 1;
		}
		printf("Hello, World! %d\n", a);
		return 0;
}
