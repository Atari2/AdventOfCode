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
#include <cmath>

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


int64_t check_word_p1(const std::vector<std::string>& data, int64_t i, int64_t j) {
    constexpr static std::string_view word_to_find = "XMAS";
    constexpr static std::array<std::pair<int64_t, int64_t>, 8> offsets{{ {0, 1}, {1, 0}, {1, 1}, {1, -1}, {0, -1}, {-1, 0}, {-1, -1}, {-1, 1} }};
    int64_t count = 0;
    if (data[i][j] != word_to_find[0]) {
        return 0;
    }
    for (const auto& [sxoff, syoff] : offsets) {
        int64_t cnt = 0;
        for (const auto& [off, c] : v::enumerate(word_to_find | v::drop(1))) {
            int64_t xoff = sxoff == 0 ? sxoff : sxoff + static_cast<int64_t>(std::copysign(off, sxoff));
            int64_t yoff = syoff == 0 ? syoff : syoff + static_cast<int64_t>(std::copysign(off, syoff));
            if (i + xoff < 0 || i + xoff >= data.size() || j + yoff < 0 || j + yoff >= data[i].size()) {
                break;
            }
            if (data[i + xoff][j + yoff] != c) {
                break;
            }
            cnt++;
        }
        if (cnt == word_to_find.size() - 1) {
            count++;
        }
    }
    return count;
}

int64_t check_word_p2(const std::vector<std::string>& data, int64_t i, int64_t j) {
    constexpr static std::array<std::pair<std::pair<int64_t, int64_t>, std::pair<int64_t, int64_t>>, 2> offsets{{ {{1, 1}, {-1, -1}}, {{-1, 1}, {1, -1}} }};
    if (data[i][j] != 'A') {
        return 0;
    }
    for (const auto& [p1, p2] : offsets) {
        const auto& [sxoff1, syoff1] = p1;
        const auto& [sxoff2, syoff2] = p2;
        if (i + sxoff1 < 0 || i + sxoff1 >= data.size() || j + syoff1 < 0 || j + syoff1 >= data[i].size()) {
            return 0;
        }
        if (i + sxoff2 < 0 || i + sxoff2 >= data.size() || j + syoff2 < 0 || j + syoff2 >= data[i].size()) {
            return 0;
        }
        if ((data[i + sxoff1][j + syoff1] == 'M' && data[i + sxoff2][j + syoff2] == 'S') || (data[i + sxoff1][j + syoff1] == 'S' && data[i + sxoff2][j + syoff2] == 'M')) {
            continue;
        }
        return 0;
    }
    return 1;
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    auto&& [p1, p2] = r::fold_left(v::cartesian_product(v::iota(size_t{0}, lines.size()), v::iota(size_t{0}, lines[0].size())), std::pair{0LL, 0LL}, [&](auto&& accum, auto&& val) {
        auto&& [i, j] = val;
        auto&& [p1, p2] = accum;
        return std::make_pair(p1 + check_word_p1(lines, i, j), p2 + check_word_p2(lines, i, j));
    });
    std::println("{} {}", p1, p2);
}