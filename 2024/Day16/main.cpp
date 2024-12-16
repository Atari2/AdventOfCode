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
#include <queue>
#include <utility>
#include <chrono>

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

using matrix = std::vector<std::string>;
using point = std::pair<int64_t, int64_t>;
using direction = std::tuple<int64_t, int64_t, char>;
using pqitem = std::tuple<int64_t, int64_t, int64_t, char, std::vector<point>>;

point find_value(const matrix& m, char value) {
    for (size_t i = 0; i < m.size(); ++i) {
        for (size_t j = 0; j < m[i].size(); ++j) {
            if (m[i][j] == value) {
                return {i, j};
            }
        }
    }
    return {-1, -1};
}

template <>
struct std::greater<pqitem> {
    bool operator()(const pqitem& lhs, const pqitem& rhs) const {
        const auto& [lhs_cost, lhs_x, lhs_y, lhs_dir, lhs_path] = lhs;
        const auto& [rhs_cost, rhs_x, rhs_y, rhs_dir, rhs_path] = rhs;
        if (lhs_cost != rhs_cost) {
            return lhs_cost > rhs_cost;
        }
        if (lhs_x != rhs_x) {
            return lhs_x > rhs_x;
        }
        if (lhs_y != rhs_y) {
            return lhs_y > rhs_y;
        }
        if (lhs_dir != rhs_dir) {
            return lhs_dir > rhs_dir;
        }
        return lhs_path.size() > rhs_path.size();
    }
};

template <>
struct std::hash<direction> {
    constexpr static inline std::hash<int64_t> hasher{};
    constexpr static inline std::hash<char> chasher{};
    std::size_t operator()(const direction& dir) const {
        const auto& [x, y, c] = dir;
        auto res = 0x345678L;
        int64_t mult = 1000003L;

        res = (res ^ hasher(x)) * mult;
        mult += 69068L + 6;

        res = (res ^ hasher(y)) * mult;
        mult += 69068L + 4;

        res = (res ^ chasher(c)) * mult;
        mult += 69068L + 2;

        return res;
    }
};

std::pair<int64_t, std::vector<std::vector<point>>> find_shortest_path(const matrix& m, point start, point end, char start_direction) {
    const auto rows = m.size();
    const auto cols = m[0].size();
    const std::unordered_map<char, std::array<direction, 3>> directions{
        {'N', std::array<direction, 3>{std::make_tuple(-1, 0, 'N'), {0, 1, 'E'}, {0, -1, 'W'}}},
        {'S', std::array<direction, 3>{std::make_tuple(1, 0, 'S'), {0, -1, 'W'}, {0, 1, 'E'}}},
        {'W', std::array<direction, 3>{std::make_tuple(0, -1, 'W'), {-1, 0, 'N'}, {1, 0, 'S'}}},
        {'E', std::array<direction, 3>{std::make_tuple(0, 1, 'E'), {1, 0, 'S'}, {-1, 0, 'N'}}},
    };
    std::priority_queue<pqitem, std::vector<pqitem>, std::greater<pqitem>> pq{};
    pq.push({0, start.first, start.second, start_direction, {}});
    std::unordered_map<direction, int64_t> visited{};
    int64_t min_cost = std::numeric_limits<int64_t>::max();
    std::vector<std::vector<point>> all_paths{};

    while (pq.size()) {
        auto [cost, row, col, prev_orientation, path] = pq.top();
        pq.pop();
        path.push_back({row, col});
        if (row == end.first && col == end.second) {
            if (cost < min_cost) {
                min_cost = cost;
                all_paths.clear();
            }
            if (cost == min_cost) {
                all_paths.push_back(path);
            }
            continue;
        }
        if (auto it = visited.find({row, col, prev_orientation}); it != visited.end() && it->second < cost) {
            continue;
        }
        visited[{row, col, prev_orientation}] = cost;
        for (const auto& [dr, dc, orientation] : directions.at(prev_orientation)) {
            auto new_row = row + dr;
            auto new_col = col + dc;
            if (new_row < 0 || new_row >= rows || new_col < 0 || new_col >= cols || m[new_row][new_col] == '#') {
                continue;
            }
            auto new_cost = cost + 1 + (prev_orientation == orientation ? 0 : 1000);
            pq.push({new_cost, new_row, new_col, orientation, path});
        }
    }
    return std::make_pair(min_cost, std::move(all_paths));
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    auto start_tile = find_value(lines, 'S');
    auto end_tile = find_value(lines, 'E');
    auto [part1, paths] = find_shortest_path(lines, start_tile, end_tile, 'E');
    auto flattened_paths = std::move(paths) | v::join | r::to<std::vector>();
    r::sort(flattened_paths);
    auto un = r::unique(flattened_paths);
    flattened_paths.erase(un.begin(), un.end());
    std::println("{} {}", part1, flattened_paths.size());
}