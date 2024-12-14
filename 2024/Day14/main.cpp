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

constexpr int64_t SPACE_HEIGHT = SAMPLE_DATA ? 7 : 103;
constexpr int64_t SPACE_WIDTH = SAMPLE_DATA ? 11 : 101;
constexpr int64_t QUADRANT_HEIGHT = SPACE_HEIGHT / 2;
constexpr int64_t QUADRANT_WIDTH = SPACE_WIDTH / 2;

using point = std::pair<int64_t, int64_t>;

int64_t mod(int64_t a, int64_t b) {
    return (a % b + b) % b;
}

struct Robot {
    point position;
    point velocity;

    Robot(const std::string& line) {
        std::sscanf(line.c_str(), "p=%" SCNd64 ",%" SCNd64 " v=%" SCNd64 ",%" SCNd64, &position.first, &position.second, &velocity.first, &velocity.second);
    }

    void move(int64_t steps = 1) {
        position.first = mod(position.first + velocity.first * steps, SPACE_WIDTH);
        position.second = mod(position.second + velocity.second * steps, SPACE_HEIGHT);
    }
};

int64_t part1(const std::vector<std::string>& lines) {
    std::array<std::array<uint8_t, SPACE_WIDTH>, SPACE_HEIGHT> space{};
    auto robots = lines | v::transform([](const auto& line) { return Robot(line); }) | r::to<std::vector>();
    for (auto& r : robots) {
        r.move(100);
        space[r.position.second][r.position.first] += 1;
    }
    std::array<int64_t, 4> quadrants{};
    for (size_t i = 0; i < SPACE_HEIGHT; ++i) {
        if (i == QUADRANT_HEIGHT) continue;
        for (size_t j = 0; j < SPACE_WIDTH; ++j) {
            if (j == QUADRANT_WIDTH) continue;
            if (auto val = space[i][j]; val > 0) {
                if (i < QUADRANT_HEIGHT && j < QUADRANT_WIDTH) {
                    quadrants[0] += val;
                } else if (i < QUADRANT_HEIGHT && j > QUADRANT_WIDTH) {
                    quadrants[1] += val;
                } else if (i > QUADRANT_HEIGHT && j < QUADRANT_WIDTH) {
                    quadrants[2] += val;
                } else {
                    quadrants[3] += val;
                }
            }
        }
    }
    return r::fold_left(quadrants, std::int64_t{1}, [](auto acc, auto val) { return val != 0 ? acc * val : acc; });
}

int64_t part2(const std::vector<std::string>& lines) {
    if constexpr (SAMPLE_DATA) return 0;
    std::array<std::array<uint8_t, SPACE_WIDTH>, SPACE_HEIGHT> space{};
    auto robots = lines | v::transform([](const auto& line) { return Robot(line); }) | r::to<std::vector>();
    for (const auto& r : robots) {
        space[r.position.second][r.position.first] += 1;
    }
    int64_t i = 0;
    while (true) {
        i += 1;
        for (auto& r : robots) {
            space[r.position.second][r.position.first] -= 1;
            r.move();
            space[r.position.second][r.position.first] += 1;
        }
        for (const auto &row : space) {
            size_t max_consecutive = 0;
            size_t consecutive = 0;
            for (const auto col : row) {
                if (col > 0) {
                    consecutive += 1;
                } else {
                    max_consecutive = std::max(max_consecutive, consecutive);
                    consecutive = 0;
                }
            }
            max_consecutive = std::max(max_consecutive, consecutive);
            if (max_consecutive >= 20) { 
                // heuristically assume that any run of 20 consecutive robots or more is part of a christmas tree.
                return i;
            }
        }
    }
}


int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    std::println("{} {}", part1(lines), part2(lines));
}