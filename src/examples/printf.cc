#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"

int main()
{
  // single-threaded programs override this function.
  printf("Hello, World from MAIN !\n");
  return 0; // the value returned is the value written to tohost?
}
