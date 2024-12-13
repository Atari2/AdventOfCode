#include <algorithm>
#include <charconv>
#include <fstream>
#include <ranges>
#include <string>
#include <string_view>
#include <unordered_map>
#include <vector>
#include <cstdio>
#include <numeric>
#include <print>
#include <cinttypes>

namespace r = std::ranges;
namespace v = std::ranges::views;
using namespace std::string_view_literals;

constexpr bool SAMPLE_DATA = false;

std::vector<std::string> read_file(std::string_view filename) {
    std::ifstream file(filename.data());
    std::vector<std::string> lines;
    std::string line;
    while (std::getline(file, line)) {
        lines.push_back(line);
    }
    return lines;
}

enum class Part { One, Two };

constexpr static uint64_t A_TOKENS_PRICE = 3;
constexpr static uint64_t B_TOKENS_PRICE = 1;

struct Machine {
    double ax;
    double ay;
    double bx;
    double by;
    double prizex;
    double prizey;

    uint64_t solve(Part part) const {
        double prizex = this->prizex;
        double prizey = this->prizey;
        if (part == Part::Two) {
            prizex += 10000000000000.0;
            prizey += 10000000000000.0;
        }
        double determinant = ax * by - ay * bx;
        if (determinant == 0) {
            return 0;
        }
        double x = (prizex * by - prizey * bx) / determinant;
        double y = (ax * prizey - ay * prizex) / determinant;
        if (std::nearbyint(x) == x && std::nearbyint(y) == y) {
            return static_cast<uint64_t>(x) * A_TOKENS_PRICE + static_cast<uint64_t>(y) * B_TOKENS_PRICE;
        }
        return 0;
    }
};

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    std::vector<Machine> machines;
    auto lit = lines.begin();
    while (lit != lines.end()) {
        Machine machine;
        std::sscanf(lit->c_str(), "Button A: X+%lf, Y+%lf", &machine.ax, &machine.ay);
        ++lit;
        std::sscanf(lit->c_str(), "Button B: X+%lf, Y+%lf", &machine.bx, &machine.by);
        ++lit;
        std::sscanf(lit->c_str(), "Prize: X=%lf, Y=%lf", &machine.prizex, &machine.prizey);
        ++lit;
        machines.push_back(machine);
        while (lit != lines.end() && lit->empty()) {
            ++lit;
        }
    }
    auto part1 = r::fold_left(machines, uint64_t{0}, [](uint64_t acc, const Machine& m) {
        return acc + m.solve(Part::One);
    });
    auto part2 = r::fold_left(machines, uint64_t{0}, [](uint64_t acc, const Machine& m) {
        return acc + m.solve(Part::Two);
    });
    std::println("{} {}", part1, part2);
}