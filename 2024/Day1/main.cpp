
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

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    std::vector<int64_t> left(lines.size());
    std::vector<int64_t> right(lines.size());
    r::for_each(lines | v::transform([](auto&& s) {
        return s | v::split("   "sv) | v::transform([](auto&& s) { 
            int64_t val;
            std::from_chars(s.data(), s.data() + s.size(), val);
            return val;
        });
    }), [&](auto&& v) {
        auto it = v.begin();
        left.push_back(*it);
        right.push_back(*++it);
    });
    r::sort(left);
    r::sort(right);
    int64_t totsum = r::fold_left(std::views::zip(left, right), 0, [](const auto& acc, const auto& p) {
        const auto& [l, r] = p;
        return acc + std::abs(l - r);
    });

    int64_t simscore = r::fold_left(left, 0, [&](const auto& acc, const auto& n) {
        return acc + n * r::count(right, n);
    });
    std::println("{} {}", totsum, simscore);
}