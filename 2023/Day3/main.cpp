// compile with: cl /nologo /O2 /EHsc /std:c++latest main.cpp
// most of this is just me playing around with C++23 ranges and views
#include <version>
#if __cpp_lib_ranges < 202207L
#error "This code requires C++23 range features"
#endif

#include <algorithm>
#include <charconv>
#include <fstream>
#include <ranges>
#include <string>
#include <string_view>
#include <vector>
#include <cstdio>
#include <unordered_map>
#include <iostream>

constexpr bool SAMPLE_DATA = false;

namespace r = std::ranges;
namespace v = std::ranges::views;
using namespace std::string_view_literals;

std::vector<std::string> read_file(std::string_view filename) {
    std::ifstream file(filename.data());
    std::vector<std::string> lines;
    std::string line;
    while (std::getline(file, line)) {
        lines.push_back(line);
    }
    return lines;
}

using Point = std::pair<int64_t, int64_t>;

template <>
struct std::hash<Point> {
    static size_t s_cols;
    static void seed(size_t cols) noexcept {
        s_cols = cols;
    }
    size_t operator()(const Point& p) const noexcept {
        return p.first * s_cols + p.second;
    }
};

size_t std::hash<Point>::s_cols = 0;

constexpr std::array<Point, 8> ADJACENCY_LIST {{
    {-1, -1}, {-1, 0}, {-1, 1},
    {0, -1}, {0, 1},
    {1, -1}, {1, 0}, {1, 1}
}};

using Gears = std::unordered_map<Point, std::vector<int64_t>>;

bool is_symbol(char c) {
    return !(std::isdigit(c) || c == '.');
}

std::pair<int64_t, Gears> get_schem_nums(const std::vector<std::string>& data) {
    int64_t schem_nums = 0;
    Gears gears{};
    const auto rows = data.size();
    const auto cols = data[0].size();
    Point pos = {-1, -1};
    bool is_to_include = false;
    std::vector<Point> gear_point{};
    for (size_t x = 0; x < rows; ++x) {
        for (size_t y = 0; y < cols; ++y) {
            if (std::isdigit(data[x][y])) {
                for (const auto& [dx, dy] : ADJACENCY_LIST) {
                    const auto inxbounds = x + dx >= 0 && x + dx < rows;
                    const auto inybounds = y + dy >= 0 && y + dy < cols;
                    if (inxbounds && inybounds && is_symbol(data[x + dx][y + dy])) {
                        if (data[x + dx][y + dy] == '*') {
                            gear_point.push_back({x + dx, y + dy});
                        }
                        is_to_include = true;
                        break;
                    }
                }
                if (auto& [px, py] = pos; px == -1 && py == -1) {
                    px = x;
                    py = y;
                }
            } else {
                if (auto& [px, py] = pos; px != -1 && py != -1) {
                    if (is_to_include) {
                        int64_t schem_num = 0;
                        std::from_chars(data[px].data() + py, data[px].data() + y, schem_num);
                        schem_nums += schem_num;
                        for (const auto& p : gear_point) {
                            auto& v = gears[p];
                            if (r::find(v, schem_num) == v.end()) {
                                v.push_back(schem_num);
                            }
                        }
                    }
                    px = -1;
                    py = -1;
                    is_to_include = false;
                    gear_point.clear();
                }
            }
        }
        if (auto& [px, py] = pos; px != -1 && py != -1) {
            if (is_to_include) {
                int64_t schem_num = 0;
                std::from_chars(data[px].data() + py, data[px].data() + data[px].size(), schem_num);
                schem_nums += schem_num;
                for (const auto& p : gear_point) {
                    auto& v = gears[p];
                    if (r::find(v, schem_num) == v.end()) {
                        v.push_back(schem_num);
                    }
                }
            }
            px = -1;
            py = -1;
            is_to_include = false;
            gear_point.clear();
        }
    }
    return {schem_nums, gears};
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt" : "data.txt");
    std::hash<Point>::seed(lines[0].size());
    auto [totalp1, gears] = get_schem_nums(lines);
    auto totalp2 = r::fold_left(gears | v::values | v::transform([](auto&& v) { return v.size() == 2 ? v[0] * v[1] : 0;}), int64_t{0}, std::plus<>{});
    std::printf("%lld %lld", totalp1, totalp2);
    return 0;
}