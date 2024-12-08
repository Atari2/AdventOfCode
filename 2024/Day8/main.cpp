#include <algorithm>
#include <charconv>
#include <fstream>
#include <ranges>
#include <string>
#include <string_view>
#include <vector>
#include <cstdio>
#include <unordered_set>
#include <numeric>
#include <print>
#if __cpp_lib_generator	== 202207L
#include <generator>
#endif


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

constexpr const std::string_view all_chars{"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"};

using point = std::pair<int64_t, int64_t>;

template <>
struct std::hash<point> {
    size_t operator()(const point& p) const {
        return std::hash<int64_t>{}(p.first) ^ std::hash<int64_t>{}(p.second);
    }
};

std::vector<point> argwhere(const std::vector<std::string>& data, char c) {
    std::vector<point> result;
    const size_t rows = data.size();
    const size_t cols = data[0].size();
    result.reserve((rows * cols) / 10); // preallocate 10% of the entire matrix, assuming ~10% of the data is the character
    for (int64_t i = 0; i < rows; i++) {
        for (int64_t j = 0; j < cols; j++) {
            if (data[i][j] == c) {
                result.emplace_back(i, j);
            }
        }
    }
    return result;
}
#if __cpp_lib_generator	== 202207L
std::generator<std::pair<point, point>> combinations(const std::vector<point>& points) {
    for (size_t i = 0; i < points.size(); i++) {
        for (size_t j = i + 1; j < points.size(); j++) {
            co_yield std::make_pair(points[i], points[j]);
        }
    }
}
#else
std::vector<std::pair<point, point>> combinations(const std::vector<point>& points) {
    std::vector<std::pair<point, point>> result;
    result.reserve(points.size() * (points.size() - 1) / 2);
    for (size_t i = 0; i < points.size(); i++) {
        for (size_t j = i + 1; j < points.size(); j++) {
            result.emplace_back(points[i], points[j]);
        }
    }
    return result;
}
#endif

int64_t part1(const std::vector<std::string>& data) {
    std::unordered_set<point> antinodes{};

    for (char c : all_chars) {
        auto positions = argwhere(data, c);
        for (auto [p1, p2] : combinations(positions)) {
            auto [x1, y1] = p1;
            auto [x2, y2] = p2;
            int64_t dx = x2 - x1;
            int64_t dy = y2 - y1;
            auto first_antinode = std::make_pair(x2 + dx, y2 + dy);
            auto second_antinode = std::make_pair(x1 - dx, y1 - dy);
            if (first_antinode.first >= 0 && first_antinode.first < data.size() && first_antinode.second >= 0 && first_antinode.second < data[0].size()) {
                antinodes.insert(first_antinode);
            }
            if (second_antinode.first >= 0 && second_antinode.first < data.size() && second_antinode.second >= 0 && second_antinode.second < data[0].size()) {
                antinodes.insert(second_antinode);
            }
        }
    }

    return antinodes.size();
}

int64_t part2(const std::vector<std::string>& data) {
    std::unordered_set<point> antinodes{};
    for (char c : all_chars) {
        auto positions = argwhere(data, c);
        for (auto [p1, p2] : combinations(positions)) {
            auto [x1, y1] = p1;
            auto [x2, y2] = p2;
            auto line_eq = [&](int64_t x) -> std::optional<int64_t> {
                float res = (float)((y2 - y1) * (x - x1)) / (float)(x2 - x1) + (float)y1;
                if (std::nearbyint(res) == res) {
                    return (int64_t)res;
                } 
                return std::nullopt;
            };
            for (int64_t x = 0; x < data.size(); x++) {
                auto y = line_eq(x);
                if (y.has_value() && y.value() >= 0 && y.value() < data[0].size()) {
                    antinodes.insert(std::make_pair(x, y.value()));
                }
            }
        }
    }
    return antinodes.size();
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    std::println("{} {}", part1(lines), part2(lines));
}
