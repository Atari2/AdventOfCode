
#include <algorithm>
#include <charconv>
#include <fstream>
#include <ranges>
#include <string>
#include <string_view>
#include <vector>
#include <cstdio>
#include <unordered_map>
#include <numeric>
#include <print>

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

using mat = std::vector<std::vector<uint8_t>>;

bool count_adjacent_rolls(const mat& data, std::pair<int64_t, int64_t> pos) {
    auto [r, c] = pos;
    int v = 0;
    for (int i = std::max(0ll, r - 1); i <= std::min<int64_t>(data.size() - 1, r + 1); ++i) {
        for (int j = std::max(0ll, c - 1); j <= std::min<int64_t>(data[0].size() - 1, c + 1); ++j) {
            v += data[i][j];
        }
    }
    return (v - 1) < 4;
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    mat grid;
    for (const auto& line : lines) {
        std::vector<uint8_t> row;
        for (char c : line) {
            row.push_back(c == '@' ? 1 : 0);
        }
        grid.push_back(std::move(row));
    }
    int64_t p1 = 0;
    int64_t p2 = 0;
    int turn = 0;
    while (true) {
        bool found = false;
        mat grid_copy = grid;
        for (int64_t r = 0; r < grid.size(); ++r) {
            for (int64_t c = 0; c < grid[0].size(); ++c) {
                if (grid[r][c] == 1) {
                    bool adj = count_adjacent_rolls(grid, {r, c});
                    if (turn == 0) {
                        p1 += adj;
                    }
                    p2 += adj;
                    if (adj) {
                        found = true;
                        grid_copy[r][c] = 0;
                    }
                }
            }
        }
        if (!found) {
            break;
        }
        grid = std::move(grid_copy);
        ++turn;
    }
    std::println("{} {}", p1, p2);
}