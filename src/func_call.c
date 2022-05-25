int test(){
  return 21;
}

int main(int argc, char** argv);
int main(int argc, char** argv)
{
  int b = 10+9;
  float a = b + test();
  return 0; // the value returned is the value written to tohost?
}
