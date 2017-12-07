#include <stdio.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>

int main () {

  std::unordered_map<std::string, std::vector<std::string>> Edges;
  std::unordered_map<std::string, unsigned> Weight;
  std::unordered_map<std::string, unsigned> Weight2;
  std::unordered_map<std::string, unsigned> Dist;

  std::ifstream infile("input7-2");
	
  std::string line;
  while (std::getline(infile, line)) {
    std::istringstream iss(line);
    std::string nome;
    unsigned peso;
    char x;
    iss >> nome >> x >> peso >> x;
    Weight[nome] = peso;
    Weight2[nome] = peso;

    Edges[nome];

    std::string flecha;
    iss >> flecha;
    if (flecha == "->") {
      std::string aux;
      while (getline(iss, aux, ',')) {
        std::string::iterator end_pos = std::remove(aux.begin(), aux.end(), ' ');
        aux.erase(end_pos, aux.end());

        Edges[nome].push_back(aux);
      }
    }
  }

  bool changed = true;
  while (changed) {
    changed = false;
    for (auto E : Edges) {
      if (Dist.count(E.first) != 0) continue;

      if (E.second.size() == 0) {
        Dist[E.first] = 1;
        changed = true;
      } else {
        unsigned max = 0;
        for (auto I : E.second) {
          if (Dist.count(I) == 0) goto next;
          if (Dist[I] > max) 
            max = Dist[I];
        } 
        if (max != 0) {
          changed = true;
          Dist[E.first] = max + 1;
          for (auto I : E.second) 
            Weight[E.first] += Weight[I];
        }
next:
        changed = changed;    
      }
    }
  }

  int max = 0;
  std::string maxV;

  for (auto W : Dist) {
    if (W.second > max) {
      max = W.second;
      maxV = W.first; 
    }
  }

  for (auto E : Edges) {
    if (E.second.size() > 0) {
      unsigned Peso = Weight[E.second[0]];
      for (auto N : E.second) {
        if (Peso != Weight[N]) {
          std::cout <<  E.first << " " << Dist[E.first] << "\n";
          if (Dist[E.first] == 4) {
            for (auto filho : Edges[E.first]) {
              std::cout << filho << " " << Weight[filho] << " " << Weight2[filho] << "\n";
            }
          }
/*          if (E.second.size() == 2) 
            std::cout << Dist[N] << " " << E.second[0] << " "<< Peso << " " << N << " " << Weight[N] << "\n";
          else {
            if (Peso != Weight[E.second[2]])
              std::cout << Dist[N] << " " << E.second[0] << " "<< Peso << " " << Weight2[E.second[0]] << "\n";
            else 
              std::cout << Dist[N] << " " << N << " " << Weight[N] << " " << Weight2[N] << "\n";
          } */
            
          break;
        }
      }
    }
  }

  return 0;
}
