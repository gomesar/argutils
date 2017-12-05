#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <set>
#include <cstring>

void quickSort(char *arr, int si, int ei);

/* function to check whether two strings are anagram of 
 *    each other */
bool areAnagram(char *str1, char *str2)
{
  int n1 = strlen(str1);
  int n2 = strlen(str2);

  // If length of both strings is not same, then they 
  // cannot be anagram
  if (n1 != n2)
    return false;

  // Sort both strings
  quickSort(str1, 0, n1 - 1);
  quickSort(str2, 0, n2 - 1);

  // Compare sorted strings
  for (int i = 0; i < n1;  i++)
    if (str1[i] != str2[i])
      return false;

  return true;
}

// Following functions (exchange and partition are needed
// for quickSort)
void exchange(char *a, char *b)
{
    char temp;
    temp = *a;
    *a   = *b;
    *b   = temp;
}
 
int partition(char A[], int si, int ei)
{
    char x = A[ei];
    int i = (si - 1);
    int j;
 
    for (j = si; j <= ei - 1; j++)
    {
        if(A[j] <= x)
        {
            i++;
            exchange(&A[i], &A[j]);
        }
    }
    exchange (&A[i + 1], &A[ei]);
    return (i + 1);
}
 
/* Implementation of Quick Sort
A[] --> Array to be sorted
si  --> Starting index
ei  --> Ending index
*/
void quickSort(char A[], int si, int ei)
{
    int pi;    /* Partitioning index */
    if(si < ei)
    {
        pi = partition(A, si, ei);
        quickSort(A, si, pi - 1);
        quickSort(A, pi + 1, ei);
    }
}

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
    std::vector<std::string> vec;
    fail = false;
    while (iss >> x) {
      if (pass.count(x) == 0) {
        pass.insert(x);
        vec.push_back(x);
      } else { 
        fail = true;
      }
    }
    if (!fail) {
      for (int i = 0; i < vec.size(); i++) {
        for (int j = 0; j < vec.size(); j++) {
          if (i != j) {
            if (areAnagram(vec[i].c_str(),  vec[j].c_str())) 
              fail = true;
          }
        }
      }
    }
    if(!fail) sum++;
  }
  std::cout << sum << "\n";
  return 0;
}
