// compile with: cl /nologo /O2 /EHsc /std:c++latest main.cpp
// most of this is just me playing around with C++23 ranges and views
#include <version>
#ifndef _MSC_VER
#error "This code requires an MSVC compiler"
#else
#if _MSC_VER < 1935 || !defined(_WIN64) || !_HAS_CXX23 || __cpp_lib_ranges < 202207L
#error "This code is for x64 MSVC 19.35+ only and requires C++23 features"
#endif
#endif

#include <algorithm>
#include <charconv>
#include <fstream>
#include <ranges>
#include <string>
#include <string_view>
#include <vector>
#include <cstdio>

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

int64_t part1(const std::vector<std::string>& lines) {
    auto times = split_once(lines[0], ':').second | v::split(' ') | v::filter([](auto&& s) { return !s.empty(); }) | v::transform([](auto&& s) {
        int64_t t;
        std::from_chars(s.data(), s.data() + s.size(), t);
        return t;
    });
    auto distances = split_once(lines[1], ':').second | v::split(' ') | v::filter([](auto&& s) { return !s.empty(); }) | v::transform([](auto&& s) {
        int64_t t;
        std::from_chars(s.data(), s.data() + s.size(), t);
        return t;
    });
    int64_t total = 1;
    for (auto [total_time, distance_to_beat] : v::zip(times, distances)) {
        int64_t times_beat = 0;
        for (int64_t ms = 0; ms < total_time; ++ms) {
            int64_t left_time = total_time - ms;
            int64_t distance_travelled = left_time * ms;
            if (distance_travelled > distance_to_beat) {
                times_beat += 1;
            }
        }
        total *= times_beat;
    }
    return total;
} 

int64_t part2(const std::vector<std::string>& lines) {
    auto timestr = split_once(lines[0], ':').second | v::split(' ') | v::filter([](auto&& s) { return !s.empty(); }) | v::transform([](auto&& s) {
        return std::string{s.begin(), s.end()};
    }) | v::join | r::to<std::string>();
    int64_t time = 0;
    std::from_chars(timestr.data(), timestr.data() + timestr.size(), time);
    auto distancestr = split_once(lines[1], ':').second | v::split(' ') | v::filter([](auto&& s) { return !s.empty(); }) | v::transform([](auto&& s) {
        return std::string{s.begin(), s.end()};
    }) | v::join | r::to<std::string>();
    int64_t distance = 0;
    std::from_chars(distancestr.data(), distancestr.data() + distancestr.size(), distance);
    int64_t times_beat = 0;
    for (int64_t ms = 0; ms < time; ++ms) {
        int64_t left_time = time - ms;
        int64_t distance_travelled = left_time * ms;
        if (distance_travelled > distance) {
            times_beat += 1;
        }
    }
    return times_beat;
} 

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt" : "data.txt");
    if (lines.size() != 2) {
        return 1;
    }
    std::printf("%lld %lld", part1(lines), part2(lines));
}