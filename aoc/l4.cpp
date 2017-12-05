#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <set>

int main () {
  std::string x;
  int largets, smallest;
  int first = 0;
  int sum = 0;
  bool fail;

  std::ifstream infile("input");
  std::string line;
  while (std::getline(infile, line)) {
    std::vector<int> numbers;
    std::istringstream iss(line);
    std::set<std::string> pass;
    fail = false;
    while (iss >> x) {
      if (pass.count(x) == 0)
        pass.insert(x);
      else 
        fail = true;
    }
    if(!fail) sum++;
  }
  std::cout << sum << "\n";
  return 0;
}
