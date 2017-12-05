#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

int main () {
  int x;
  int largets, smallest;
  int first = 0;
  int sum = 0;

  std::ifstream infile("spreadsheet");
  std::string line;
  while (std::getline(infile, line)) {
    std::istringstream iss(line);
    first = 0;
    while (iss >> x) {
      if (first == 0) {
        largets = x;
        smallest = x;
        first = 1;
      }

      if (x > largets) largets = x;
      if (x < smallest) smallest = x;
    }
    sum += (largets - smallest);
  }
  std::cout <<  sum << "\n";
  return 0;
}
