#include <algorithm>
#include <charconv>
#include <fstream>
#include <ranges>
#include <string>
#include <string_view>
#include <unordered_set>
#include <vector>
#include <cstdio>
#include <numeric>
#include <print>
#include <cinttypes>
#include <queue>
#include <utility>
#include <chrono>

namespace r = std::ranges;
namespace v = std::ranges::views;
using namespace std::string_view_literals;

constexpr bool SAMPLE_DATA = false;
constexpr size_t GRID_SIZE = SAMPLE_DATA ? 6+1 : 70+1;
constexpr size_t NUM_FALLING_BYTES = SAMPLE_DATA ? 12 : 1024;

std::vector<std::string> read_file(std::string_view filename) {
    std::ifstream file(filename.data());
    std::vector<std::string> lines;
    std::string line;
    while (std::getline(file, line)) {
        lines.push_back(line);
    }
    return lines;
}

using matrix = std::vector<std::vector<int64_t>>;
using point = std::pair<int64_t, int64_t>;

template <>
struct std::hash<point> {
    constexpr static inline std::hash<int64_t> hasher{};
    std::size_t operator()(const point& dir) const {
        const auto& [x, y] = dir;
        auto res = 0x345678L;
        int64_t mult = 1000003L;

        res = (res ^ hasher(x)) * mult;
        mult += 69068L + 4;

        res = (res ^ hasher(y)) * mult;
        mult += 69068L + 2;

        return res;
    }
};

int64_t find_shortest_path(const matrix& m, point start, point end) {
    point directions[] = {
        point{-1, 0},
        point{1, 0},
        point{0, -1},
        point{0, 1},
    };
    std::deque<std::pair<point, int64_t>> queue{std::make_pair(start, 0)};
    std::unordered_set<point> visited{};
    visited.insert(start);

    while (queue.size()) {
        auto [pos, steps] = queue.front();
        auto [current_row, current_col] = pos;
        queue.pop_front();
        if (pos == end) {
            return steps;
        }
        for (const auto& [row_offset, col_offset] : directions) {
            auto neighbor_row = current_row + row_offset;
            auto neighbor_col = current_col + col_offset;
            auto neighbor_pos = point{neighbor_row, neighbor_col};
            if (neighbor_row >= 0 && neighbor_row < GRID_SIZE && neighbor_col >= 0 && neighbor_col < GRID_SIZE 
                && m[neighbor_row][neighbor_col] == 0
                && !visited.contains(neighbor_pos)) {
                visited.insert(neighbor_pos);
                queue.push_back({neighbor_pos, steps + 1});
            }
        }
    }

    return -1;
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    auto bytes = lines | v::transform([](auto&& str) {
        int64_t x, y;
        std::sscanf(str.data(), "%" SCNd64 ", %" SCNd64, &x, &y);
        return point{y, x};
    }) | r::to<std::vector>();
    auto grid = matrix(GRID_SIZE, std::vector<int64_t>(GRID_SIZE, 0));
    auto starting_position = point{0, 0};
    auto ending_position = point{GRID_SIZE - 1, GRID_SIZE - 1};
    std::span<point> falling_bytes{bytes.begin(), NUM_FALLING_BYTES};
    for (const auto& [row, col] : falling_bytes) {
        grid[row][col] = 1;
    }
    auto shortest_path = find_shortest_path(grid, starting_position, ending_position);

    point part2{};
    std::span<point> remaining_bytes{bytes.begin() + NUM_FALLING_BYTES, bytes.size() - NUM_FALLING_BYTES};
    for (const auto& [row, col] : remaining_bytes) {
        grid[row][col] = 1;
        if (find_shortest_path(grid, starting_position, ending_position) == -1) {
            part2 = {col, row};
            break;
        }
    }

    std::println("{} {},{}", shortest_path, part2.first, part2.second);
}