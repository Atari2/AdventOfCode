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
#include <span>
#include <complex>

namespace r = std::ranges;
namespace v = std::ranges::views;
using namespace std::string_view_literals;
using namespace std::complex_literals;

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

static std::unordered_map<char, std::complex<double>> numpad{{
    {'7', 0.0 + 0i},
    {'8', 1.0 + 0i},
    {'9', 2.0 + 0i},
    {'4', 0.0 + 1i},
    {'5', 1.0 + 1i},
    {'6', 2.0 + 1i},
    {'1', 0.0 + 2i},
    {'2', 1.0 + 2i},
    {'3', 2.0 + 2i},
    {' ', 0.0 + 3i},
    {'0', 1.0 + 3i},
    {'A', 2.0 + 3i},  
}};

static std::unordered_map<char, std::complex<double>> robot{{
    {' ', 0.0 + 0i}, 
    {'^', 1.0 + 0i}, 
    {'A', 2.0 + 0i}, 
    {'<', 0.0 + 1i}, 
    {'v', 1.0 + 1i}, 
    {'>', 2.0 + 1i}
}};

template <>
struct std::hash<std::pair<char, char>> {
    static constexpr inline std::hash<char> hash_str{};
    std::size_t operator()(const std::pair<char, char>& p) const {
        return hash_str(p.first) ^ hash_str(p.second);
    }
};

template <>
struct std::hash<std::tuple<std::string, int64_t, int64_t>> {
    static constexpr inline std::hash<std::string> hash_str{};
    static constexpr inline std::hash<int64_t> hash_int{};
    std::size_t operator()(const std::tuple<std::string, int64_t, int64_t>& p) const {
        return hash_str(std::get<0>(p)) ^ hash_int(std::get<1>(p)) ^ hash_int(std::get<2>(p));
    }
};

static std::unordered_map<std::pair<char, char>, std::string> path_cache{};
static std::unordered_map<std::tuple<std::string, int64_t, int64_t>, int64_t> length_cache{};

std::string path(char start, char end) {
    auto pair = std::make_pair(start, end);
    if (auto it = path_cache.find(pair); it != path_cache.end()) {
        return it->second;
    }
    const auto& pad = (numpad.contains(start) && numpad.contains(end)) ? numpad : robot;
    auto diff = pad.at(end) - pad.at(start);
    auto dx = static_cast<int64_t>(diff.real());
    auto dy = static_cast<int64_t>(diff.imag());
    auto yy = dy < 0 ? std::string(-dy, '^') : std::string(dy, 'v');
    auto xx = dx < 0 ? std::string(-dx, '<') : std::string(dx, '>');
    auto bad = pad.at(' ') - pad.at(start);
    auto prefer_yy_first = (dx > 0 || bad == static_cast<double>(dx)) && bad != static_cast<double>(dy) * 1i;
    auto result = (prefer_yy_first ? yy + xx : xx + yy) + "A";
    path_cache[pair] = result;
    return result;
}

int64_t length(const std::string& code, int64_t depth, int64_t s = 0) {
    auto tuple = std::make_tuple(code, depth, s);
    if (auto it = length_cache.find(tuple); it != length_cache.end()) {
        return it->second;
    }
    if (depth == 0) {
        return code.size();
    }
    for (auto&& [i, c] : code | v::enumerate) {
        s += length(path(i > 0 ? code[i - 1] : code.back(), c), depth - 1);
    }
    length_cache[tuple] = s;
    return s;
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    auto part1 = r::fold_left(lines, 0, [](int64_t acc, const std::string& code) {
        int64_t val{};
        std::from_chars(code.data(), code.data() + code.size() - 1, val);
        return acc + val * length(code, 3);
    });
    auto part2 = r::fold_left(lines, 0, [](int64_t acc, const std::string& code) {
        int64_t val{};
        std::from_chars(code.data(), code.data() + code.size() - 1, val);
        return acc + val * length(code, 26);
    });
    std::println("{} {}", part1, part2);
}