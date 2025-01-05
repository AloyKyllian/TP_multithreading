#include <cpr/cpr.h>
#include <iostream>
using namespace std;
#include <Eigen/Core>
#include <Eigen/Dense>
#include <fstream>
#include <nlohmann/json.hpp>
using namespace Eigen;
#include <chrono>
using json = nlohmann::json;

const int SIZE_FIX = 100;

class Task {
public:
  int identifier;
  int size;
  Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic, Eigen::ColMajor> a;
  VectorXf b;
  VectorXf x;
  float time;

public:
  Task(
      int id, int s,
      Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic, Eigen::ColMajor> &a1,
      VectorXf &b1, VectorXf &x1, float t) {
    this->identifier = id;
    this->size = s;
    this->a = a1;
    this->b = b1;
    this->x = x1;
    this->time = t;
  };

  json to_json() {
    json j;
    j["identifier"] = this->identifier;
    j["size"] = this->size;

    j["a"] = json::array(); // Crée un tableau JSON
    for (int i = 0; i < size; ++i) {
      std::vector<float> row(
          a(i), a(i) + size); // Convertir chaque ligne en un vecteur
      j["a"].push_back(row);  // Ajouter chaque ligne au tableau 'a'
    }
    j["b"] = this->b;
    j["x"] = this->x;
    j["time"] = this->time;

    return j;
  };

public:
  static Task from_json(json j_data) {
    int id = j_data["identifier"];
    int size = j_data["size"];

    Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic, Eigen::ColMajor> a(
        100, 100);
    for (int i = 0; i < size; ++i) {
      for (int j = 0; j < size; ++j) {
        a(i, j) = j_data["a"][i][j];
      }
    }

    VectorXf b(size);
    VectorXf x(size);
    for (int i = 0; i < size; ++i) {
      b(i) = j_data["b"][i];
      x(i) = j_data["x"][i];
    }

    float time = j_data["time"];

    // Création et retour de l'objet Task
    Task task = Task(id, size, a, b, x, time);

    return task;
  };

  void work() {
    Eigen::setNbThreads(12);
    std::cout << "Using " << Eigen::nbThreads()
              << " threads for Eigen operations.\n";
    auto start = std::chrono::high_resolution_clock::now();

    Eigen::VectorXf solution = this->a.householderQr().solve(this->b);

    auto end = std::chrono::high_resolution_clock::now();
    this->time = std::chrono::duration<float>(end - start).count();
    this->x = solution;
  };
};

int main(int argc, char **argv) {
  cpr::Response r = cpr::Get(cpr::Url{"http://localhost:8000"});
  r.status_code;            // 200
  r.header["content-type"]; // application/json; charset=utf-8
  json j = json::parse(r.text);
  cout << j["identifier"] << endl;

  cout << "cree task" << endl;
  Task t = Task::from_json(j);
  cout << "Work" << endl;
  t.work();
  cout << t.time << endl;
  json j2 = t.to_json();

  cpr::Response e = cpr::Post(
      cpr::Url{"http://localhost:8000"},
      cpr::Header{{"Content-Type", "application/json"}}, // En-tête HTTP
      cpr::Body{j2.dump()}                               // Corps de la requête
  );

  return 0;
}
