#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <algorithm>

const double BIG_NUMBER = 1e10;

struct Point {
    double x;
    double y;
};

struct Solution {
    std::vector<Point> points;
    double error;
};

Solution FuerzaBruta(std::vector<double>& grid_x, std::vector<double>& grid_y, std::vector<double>& x, std::vector<double>& y, int k, std::vector<Point>& sol) {
    Solution best_solution;
    best_solution.error = BIG_NUMBER;

    if (grid_x.size() < k - sol.size()) {
        best_solution.error = BIG_NUMBER;
        return best_solution;
    }

    if (sol.size() == k) {
        double error = 0.0;
        // Calculate error
        // ...
        best_solution.error = error;
        best_solution.points = sol;
        return best_solution;
    }

    for (double i : grid_y) {
        sol.push_back({grid_x[0], i});
        Solution recursion = FuerzaBruta(std::vector<double>(grid_x.begin() + 1, grid_x.end()), grid_y, x, y, k, sol);

        if (recursion.error < best_solution.error) {
            best_solution = recursion;
        }

        sol.pop_back();
    }

    if (!sol.empty()) {
        Solution recursion = FuerzaBruta(std::vector<double>(grid_x.begin() + 1, grid_x.end()), grid_y, x, y, k, sol);

        if (recursion.error < best_solution.error) {
            best_solution = recursion;
        }
    }

    return best_solution;
}

Solution BackTracking(std::vector<double>& grid_x, std::vector<double>& grid_y, std::vector<double>& x, std::vector<double>& y, int k, std::vector<Point>& sol) {
    Solution best_solution;
    best_solution.error = BIG_NUMBER;

    if (grid_x.size() < k - sol.size()) {
        best_solution.error = BIG_NUMBER;
        return best_solution;
    }

    if (sol.size() == k) {
        double error = 0.0;
        // Calculate error
        // ...
        best_solution.error = error;
        best_solution.points = sol;
        return best_solution;
    }

    if (k - sol.size() == 1) {
        grid_x = {grid_x.back()};
    }

    for (double i : grid_y) {
        sol.push_back({grid_x[0], i});

        double current_error = 0.0;
        // Calculate error
        // ...

        if (current_error < best_solution.error) {
            Solution recursion = BackTracking(std::vector<double>(grid_x.begin() + 1, grid_x.end()), grid_y, x, y, k, sol);

            if (recursion.error < best_solution.error) {
                best_solution = recursion;
            }
        }

        sol.pop_back();
    }

    if (!sol.empty()) {
        Solution recursion = BackTracking(std::vector<double>(grid_x.begin() + 1, grid_x.end()), grid_y, x, y, k, sol);

        if (recursion.error < best_solution.error) {
            best_solution = recursion;
        }
    }

    return best_solution;
}

double CalculateError(std::vector<Point>& sol, std::vector<double>& x, std::vector<double>& y) {
    double error = 0.0;
    // Calculate error
    // ...
    return error;
}

void Main() {
    std::vector<std::string> jsons = {"aspen_simulation.json", "ethanol_water_vle.json", "optimistic_instance.json", "titanium.json", "toy_instance.json"};
    std::string instance_name = "optimistic_instance.json";
    std::string filename = "data/" + instance_name;
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error: Unable to open file " << filename << std::endl;
        return;
    }

    // Read instance from JSON
    // ...
    
    int K = instance["n"];
    int m = 6;
    int n = 6;
    int N = 5;

    std::vector<double> grid_x(m);
    std::vector<double> grid_y(n);
    std::vector<double> x = instance["x"];
    std::vector<double> y = instance["y"];

    // Generate grid
    // ...

    std::vector<Point> sol;
    Solution fuerza_bruta_solution = FuerzaBruta(grid_x, grid_y, x, y, N, sol);
    Solution backtracking_solution = BackTracking(grid_x, grid_y, x, y, N, sol);

    std::cout << "Fuerza Bruta: error = " << fuerza_bruta_solution.error << std::endl;
    std::cout << "Backtracking: error = " << backtracking_solution.error << std::endl;

    // Save solution to JSON file
    // ...

    // Plot solution
    // ...
}

int main() {
    Main();
    return 0;
}
