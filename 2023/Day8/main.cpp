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
#include <numeric>

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

using Mappings = std::unordered_map<std::string, std::pair<std::string, std::string>>;

size_t part2(const Mappings& mappings, const std::string& instructions) {
    auto currents = mappings | v::keys | v::filter([](auto&& s) { return s.back() == 'A'; }) | r::to<std::vector>();
    std::vector<size_t> current_values{};
    current_values.reserve(currents.size());
    for (auto&& s : currents) {
        size_t index = 0;
        auto curr{std::move(s)};
        while (curr.back() != 'Z') {
            auto lr = instructions[index % instructions.size()];
            if (lr == 'L') {
                curr = mappings.at(curr).first;
            } else {
                curr = mappings.at(curr).second;
            }
            ++index;
        }
        current_values.push_back(index);
    }
    auto part2 = r::fold_left(current_values | v::drop(1), current_values.front(), [](auto&& a, auto&& b) { return std::lcm(a, b); });
    return part2;
}

size_t part1(const Mappings& mappings, const std::string& instructions) {
    std::string current{"AAA"};
    size_t index = 0;
    while (current != "ZZZ"sv) {
        auto lr = instructions[index % instructions.size()];
        if (lr == 'L') {
            current = mappings.at(current).first;
        } else {
            current = mappings.at(current).second;
        }
        ++index;
    }
    return index;
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    Mappings mappings{};
    auto iter = lines.begin();
    const auto& instructions = *iter++;
    while (iter != lines.end()) {
        if (iter->empty()) {
            ++iter;
            continue;
        };
        char source[4], ltarget[4], rtarget[4];
        sscanf_s(iter->c_str(), "%3s = (%3s, %3s)", source, 4, ltarget, 4, rtarget,4);
        mappings.emplace(source, std::make_pair(ltarget, rtarget));
        ++iter;
    }
   
    std::printf("%zu %zu\n", part1(mappings, instructions), part2(mappings, instructions));
    return 0;
}