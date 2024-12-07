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
#include <generator>

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

enum class Part { One, Two };
enum class Op { Add, Mul, Concat };

std::generator<std::vector<Op>> product(r::range auto&& v, size_t repeat, std::vector<Op> current = {}) {
    if (current.size() == repeat) {
        co_yield current;
    } else {
        for (const auto& item : v) {
            current.push_back(item); 
            for (const auto& result : product(v, repeat, current)) {
                co_yield result;
            }
            current.pop_back();
        }
    }
}

uint64_t concatenate(uint64_t a, uint64_t b) {
    static constexpr const uint64_t powersOfTen[] = {
        1, 10, 100, 1000, 10000, 100000, 1000000,
        10000000, 100000000, 1000000000, 10000000000,
        100000000000, 1000000000000, 10000000000000,
        100000000000000, 1000000000000000, 10000000000000000,
        100000000000000000, 1000000000000000000
    };
    uint64_t digits = 0;
    if (b == 0) { 
        digits = 1; 
    } else {
        unsigned long index; 
        #ifdef _MSC_VER
        _BitScanReverse64(&index, b); 
        #else
        index = 63 - __builtin_clzll(b);
        #endif
        digits = 1 + index * 30103 / 100000;
        if (b >= powersOfTen[digits]) { ++digits; }
    }
    return a * powersOfTen[digits] + b;
}

struct Equation {
    uint64_t expected_result;
    std::vector<uint64_t> operands;
    const static inline std::vector<Op> opsp1{Op::Add, Op::Mul};
    const static inline std::vector<Op> opsp2{Op::Add, Op::Mul, Op::Concat};

    Equation(const std::string& line) {
        auto v = line | v::split(':') | v::take(2);
        auto it = v.begin();
        std::from_chars((*it).data(), (*it).data() + (*it).size(), expected_result);
        it++;
        operands = *it | v::drop_while([](char c) { return c == ' '; }) | v::split(' ') | v::transform([](auto&& s) {
            uint64_t value = 0;
            std::from_chars(s.data(), s.data() + s.size(), value);
            return value;
        }) | r::to<std::vector>();
    }  

    uint64_t solve(Part part) {
        std::span possible_ops = part == Part::One ? opsp1 : opsp2;
        for (auto&& ops : product(possible_ops, operands.size() - 1)) {
            auto result = operands.front();
            for (auto&& [op, val] : v::zip(ops, operands | v::drop(1))) {
                switch (op) {
                    case Op::Add: result += val; break;
                    case Op::Mul: result *= val; break;
                    case Op::Concat: result = concatenate(result, val); break;
                }
            }
            if (result == expected_result) {
                return result;
            }
        }
        return 0;
    }
};

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    auto equations = lines | v::transform([](auto&& line) { return Equation(line); }) | r::to<std::vector>();
    auto part1 = r::fold_left(equations | v::transform([](auto&& eq) { return eq.solve(Part::One); }), 0, std::plus{});
    auto part2 = r::fold_left(equations | v::transform([](auto&& eq) { return eq.solve(Part::Two); }), 0, std::plus{});
    std::println("{} {}", part1, part2);
}
