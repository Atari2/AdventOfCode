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
#include <span>

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

auto strip_view(std::string_view line) {
    auto first = line.find_first_not_of(" \t\n\v\f\r"sv);
    auto last = line.find_last_not_of(" \t\n\v\f\r"sv);
    return line.substr(first, last - first + 1);
}

std::pair<std::string_view, std::string_view> split_once(std::string_view orig, char delim, bool trim = true) {
    auto delim_pos = orig.find(delim);
    if (delim_pos == std::string_view::npos) {
        return {trim ? strip_view(orig) : orig, {}};
    }
    auto first = orig.substr(0, delim_pos);
    auto second = orig.substr(delim_pos + 1);
    if (trim) {
        first = strip_view(first);
        second = strip_view(second);
    }
    return {first, second};
}

using RangeType = std::ranges::subrange<std::string_view::iterator>;

struct Card {
    int64_t points{0};
    int64_t matching_numbers{0};
    int64_t total_qty{0};

    static Card fromLine(std::string_view line) {
        auto [_, numbers] = split_once(line, ':');
        auto [winning_numbers_str, total_numbers_str] = split_once(numbers, '|');
        auto winning_numbers = winning_numbers_str | v::split(' ') | v::filter([](auto&& s) { return !s.empty(); }) | v::transform(&Card::range_to_int);
        auto total_numbers = total_numbers_str | v::split(' ') | v::filter([](auto&& s) { return !s.empty(); }) | v::transform(&Card::range_to_int);
        int64_t points = calc_points(winning_numbers, total_numbers);
        int64_t matching_numbers = r::count_if(winning_numbers, [&total_numbers](auto&& n) { return r::find(total_numbers, n) != total_numbers.end(); });
        return Card{points, matching_numbers, 1};
    }

    private:
    static int64_t range_to_int(RangeType&& range) {
        int64_t n;
        auto view = strip_view(std::string_view{range});
        std::from_chars(view.data(), view.data() + view.size(), n);
        return n;
    }
    static int64_t calc_points(r::input_range auto winning_numbers, r::input_range auto total_numbers) {
        int64_t total = 0;
        for (auto n : winning_numbers) {
            if (r::find(total_numbers, n) != total_numbers.end()) {
                total = total == 0 ? 1 : total * 2;
            }
        }
        return total;
    }
};


int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt" : "data.txt");
    auto cards = lines | v::transform(&Card::fromLine) | r::to<std::vector>();
    auto totalp1 = r::fold_left(cards, 0, [](auto total, auto card) { return total + card.points; });
    for (size_t i = 0; i < cards.size(); ++i) {
        const auto& card = cards[i];
        std::span others{cards.data() + i + 1, static_cast<size_t>(card.matching_numbers)};
        for (auto& other : others) {
            other.total_qty += card.total_qty;
        }
    }
    auto totalp2 = r::fold_left(cards, 0, [](auto total, auto card) { return total + card.total_qty; });
    std::printf("%lld %lld", totalp1, totalp2);
    return 0;
}