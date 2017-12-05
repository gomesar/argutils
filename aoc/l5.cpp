#include <stdio.h>
#include <vector>

int main () {
  std::vector<int> jumps;
  int x;
  while (scanf("%d", &x) != EOF) {
    jumps.push_back(x);
  }

  int offset = 0;
  int i = 0;
  while (offset >= 0 && offset < jumps.size()) {
    int tmp = jumps[offset];
    if (tmp >= 3) {
      jumps[offset] -= 1;
    } else {
      jumps[offset] += 1;
    }
    offset = offset + tmp;
    i++;
  }
  printf("%d\n", i);
  return 0;
}
