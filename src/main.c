//--------------------------------------------------------------------------
// Main
//#include "pthread_lib.h"

//__thread unsigned executing_hartid;
//unsigned n_harts = 0;

extern int printf(const char* fmt, ...);

int test(){
  return 21;
}

int main(int argc, char** argv);
int main(int argc, char** argv)
{
  int b = 10+9;
  float a = b + test();
  asm("addi a5, a5, 0");
  asm("addi a5, a5, 0");
  asm("addi a5, a5, 0");
  asm("addi a5, a5, 0");
  asm("addi a5, a5, 0");
  asm("addi a5, a5, 0");
  // single-threaded programs override this function.
  // printf("Hello, World from MAIN !\n");
  return 0; // the value returned is the value written to tohost?
}
