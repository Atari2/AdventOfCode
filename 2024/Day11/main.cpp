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
namespace r = std::ranges;
namespace v = std::ranges::views;
using namespace std::string_view_literals;
using stone = std::pair<uint64_t, uint64_t>;
static constexpr const uint64_t powersOfTen[] = {
    1, 10, 100, 1000, 10000, 100000, 1000000,
    10000000, 100000000, 1000000000, 10000000000,
    100000000000, 1000000000000, 10000000000000,
    100000000000000, 1000000000000000, 10000000000000000,
    100000000000000000, 1000000000000000000
};
uint64_t digits(uint64_t num) {
    uint64_t digits = 0;
    if (num == 0) { 
        digits = 1; 
    } else {
        unsigned long index; 
        #ifdef _MSC_VER
        _BitScanReverse64(&index, num); 
        #else
        index = 63 - __builtin_clzll(num);
        #endif
        digits = 1 + index * 30103 / 100000;
        if (num >= powersOfTen[digits]) { ++digits; }
    }
    return digits;
}

std::pair<uint64_t, uint64_t> split_number(uint64_t number, uint64_t digits) {
    const uint64_t divisor = powersOfTen[digits / 2];
    const uint64_t rightPart = number % divisor;
    const uint64_t leftPart = number / divisor;
    return {leftPart, rightPart};
}

int main() {
    auto stones = "510613 358 84 40702 4373582 2 0 1584"sv | v::split(' ') | v::transform([](auto&& range) { 
        uint64_t value;
        std::from_chars(range.data(), range.data() + range.size(), value);
        return std::make_pair(value, uint64_t{1}); 
    }) | r::to<std::unordered_map>();
    uint64_t part1 = 0;
    for (size_t i = 0; i < 75; ++i) {
        if (i == 25) {
            part1 = r::fold_left(stones, 0, [](uint64_t acc, const auto& s) { return acc + s.second; });
        }
        std::unordered_map<uint64_t, uint64_t> new_stones{};
        for (auto&& [value, occurrences] : stones) {
            if (value == 0) {
                if (auto it = new_stones.find(1); it != new_stones.end()) {
                    it->second += occurrences;
                } else {
                    new_stones.emplace(1, occurrences);
                }
            } else if (uint64_t len = digits(value); len % 2 == 0) {
                auto [left, right] = split_number(value, len);
                if (auto it = new_stones.find(left); it != new_stones.end()) {
                    it->second += occurrences;
                } else {
                    new_stones.emplace(left, occurrences);
                }
                if (auto it = new_stones.find(right); it != new_stones.end()) {
                    it->second += occurrences;
                } else {
                    new_stones.emplace(right, occurrences);
                }
            } else {
                if (auto it = new_stones.find(value * 2024); it != new_stones.end()) {
                    it->second += occurrences;
                } else {
                    new_stones.emplace(value * 2024, occurrences);
                }
            }
        }
        stones = std::move(new_stones);
    }
    uint64_t part2 = r::fold_left(stones, 0, [](size_t acc, const auto& s) { return acc + s.second; });
    std::println("{} {}", part1, part2);
}
