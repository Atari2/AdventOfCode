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
#include <utility>

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

bool is_valid(const matrix& m, int64_t row, int64_t col) {
    return row >= 0 && row < m.size() && col >= 0 && col < m[0].size() && m[row][col] != '#';
}

int64_t manhattan(const point& a, const point& b) {
    return std::abs(a.first - b.first) + std::abs(a.second - b.second);
}

static constexpr inline std::array offsets{
    point{0, 1},
    point{0, -1},
    point{1, 0},
    point{-1, 0}
};

std::unordered_map<point, int64_t> find_path(const matrix& m, point start, point end) {
    std::unordered_map<point, int64_t> distances{};
    auto current = end;
    auto target = end;
    int64_t count = 0;
    while (start != target) {
        distances[target] = count;
        count += 1;
        for (auto [xoff, yoff] : offsets) {
            auto neighbor = point{target.first + xoff, target.second + yoff};
            if (neighbor != current && is_valid(m, neighbor.first, neighbor.second)) {
                current = target;
                target = neighbor;
                break;
            }
        }
    }
    distances[start] = count;
    return distances;
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    auto start_tile = find_value(lines, 'S');
    auto end_tile = find_value(lines, 'E');
    auto distances = find_path(lines, start_tile, end_tile);

    auto part1 = 0;
    auto part2 = 0;

    for (const auto& [p1, c1] : distances | v::reverse) {
        for (const auto& [p2, c2] : distances) {
            auto dist = manhattan(p1, p2);
            if (dist <= 2 && c2 - c1 - dist >= 100) {
                part1++;
            }
            if (dist <= 20 && c2 - c1 - dist >= 100) {
                part2++;
            }
        }
    }

    std::println("{} {}", part1, part2);
}