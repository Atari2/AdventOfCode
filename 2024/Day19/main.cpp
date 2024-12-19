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

template <>
struct std::hash<std::pair<std::string, std::string>> {
    constexpr static inline std::hash<std::string> hasher{};
    size_t operator()(const std::pair<std::string, std::string>& p) const {
        return hasher(p.first) ^ hasher(p.second);
    }
};

static std::unordered_map<std::pair<std::string, std::string>, size_t> memo{};

size_t build_all_arrangements(r::range auto&& towels, std::string&& current_arrangement, const std::string& arrangement) {
    auto pair = std::make_pair(current_arrangement, arrangement);
    if (memo.contains(pair)) {
        return memo[pair];
    }
    size_t count = 0;
    for (auto&& towel : towels) {
        auto next_arrangement = current_arrangement + std::string{towel.data(), towel.size()};
        if (next_arrangement == arrangement) {
            count += 1;
        }
        if (arrangement.starts_with(next_arrangement)) {
            if (size_t c = build_all_arrangements(towels, std::move(next_arrangement), arrangement)) {
                count += c;
            }
        }
    }
    memo.emplace(std::move(pair), count);
    return count;
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    auto towels = lines[0] | v::split(',') | v::transform([](auto&& range) {
        return range | v::drop_while([](char c) { return c == ' '; });
    });
    auto res = lines | v::drop(2) | v::transform([&](auto&& arrangement) { 
        return build_all_arrangements(towels, "", arrangement); 
    }) | v::filter([](auto&& res) { return res != 0; }) | r::to<std::vector>();
    std::println("{} {}", res.size(), r::fold_left(res, 0, std::plus{}));

}