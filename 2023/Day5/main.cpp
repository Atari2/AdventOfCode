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
#include <span>
#include <variant>

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

struct Range {
    int64_t start{0};
    int64_t stop{0};

    bool contains(int64_t value) const {
        return value >= start && value <= stop;
    }
    bool is_empty() const {
        return start >= stop;
    }
    int64_t length() const {
        return stop - start;
    }
};

struct MapRange {
    int64_t dest_range{0};
    int64_t source_range{0};
    int64_t len_range{0};

    bool contains(int64_t value) const {
        Range r{source_range, source_range + len_range};
        return r.contains(value);
    }
};

using OverlapRest = std::variant<Range, std::pair<std::optional<Range>, std::optional<Range>>>;

struct MapRanges {
    std::string_view dest_name;
    std::vector<MapRange> ranges;

    int64_t map_seed(int64_t seed) const {
        for (const auto& r : ranges) {
            if (r.contains(seed)) {
                return r.dest_range + seed - r.source_range;
            }
        }
        return seed;
    }

    std::vector<Range> map_range(Range seed_range) const {
        std::vector<Range> dest_ranges{};
        std::vector<Range> seed_ranges{seed_range};
        for (const auto& r : ranges) {
            std::vector<Range> new_seed_ranges{};
            for (const auto& sr : seed_ranges) {
                auto [o, rest] = _overlap(sr, r);
                if (o.has_value()) {
                    dest_ranges.push_back(*o);
                }
                if (Range* ptr = std::get_if<Range>(&rest); ptr != nullptr) {
                    new_seed_ranges.push_back(*ptr);
                } else {
                    auto& [ll, rr] = std::get<1>(rest);
                    if (ll.has_value()) {
                        new_seed_ranges.push_back(*ll);
                    }
                    if (rr.has_value()) {
                        new_seed_ranges.push_back(*rr);
                    }
                }
            }
            seed_ranges = std::move(new_seed_ranges);
            if (seed_ranges.empty()) {
                break;
            }
        }
        if (dest_ranges.empty()) {
            dest_ranges.push_back(seed_range);
        }
        return dest_ranges;
    }

    std::pair<std::optional<Range>, OverlapRest> _overlap(Range sr, MapRange r) const {
        std::optional<Range> output{std::nullopt};
        Range overlap{ std::max(sr.start, r.source_range), std::min(sr.stop, r.source_range + r.len_range) };
        if (auto l = overlap.length(); l > 0) {
            auto dstart = r.dest_range + overlap.start - r.source_range;
            auto dend = dstart + l;
            output = Range{dstart, dend};
            std::optional<Range> left{std::nullopt};
            std::optional<Range> right{std::nullopt};
            if (overlap.start > sr.start) {
                left = Range{sr.start, overlap.start};
            }
            if (overlap.stop < sr.stop) {
                right = Range{overlap.stop, sr.stop};
            }
            return std::make_pair(output, std::make_pair(left, right));
        }
        return std::make_pair(output, sr);
    } 

};

using VRange = std::variant<Range, std::vector<Range>>;
using it = std::vector<std::string>::iterator;
struct LocMap {
    std::unordered_map<std::string_view, MapRanges> mappers;
    static LocMap fromIter(it iter, it end) {
        LocMap locmap{};
        std::string_view source{};
        std::string_view dest{};
        while (iter != end) {
            const auto& line = *iter++;
            if (line.empty()) {
                continue;
            }
            if (auto idx = line.find("-to-"); idx != std::string::npos) {
                auto [mapping, _] = split_once(line, ' ');
                source = std::string_view{mapping}.substr(0, idx);
                dest = std::string_view{mapping}.substr(idx + 4);
                locmap.mappers[source].dest_name = dest;
            } else if (!source.empty() && !dest.empty()) {
                auto ranges = line | v::split(' ') | v::transform([](auto&& s) {
                    int64_t n;
                    std::from_chars(s.data(), s.data() + s.size(), n);
                    return n;
                }) | v::chunk(3) | v::transform([](auto&& rng) {
                    auto it = rng.begin();
                    return MapRange{*it, *(++it), *(++it)};
                });
                r::move(ranges, std::back_inserter(locmap.mappers[source].ranges));
            }
        }
        return locmap;
    }
    int64_t find_seed_location(int64_t seed) const {
        std::string_view cur_loc{"seed"};
        while (cur_loc != "location"sv) {
            const auto& rangemap = mappers.at(cur_loc);
            seed = rangemap.map_seed(seed);
            cur_loc = rangemap.dest_name;
        }
        return seed;
    }
    int64_t find_seed_range_location(Range seed_range) const {
        std::string_view cur_loc{"seed"};
        VRange cur_range{seed_range};
        while (cur_loc != "location"sv) {
            const auto& rangemap = mappers.at(cur_loc);
            if (Range* ptr = std::get_if<Range>(&cur_range); ptr != nullptr) {
                cur_range = rangemap.map_range(*ptr);
            } else {
                auto& ranges = std::get<std::vector<Range>>(cur_range);
                std::vector<Range> new_seed_ranges{};
                for (const auto& sr : ranges) {
                    auto mr = rangemap.map_range(sr);
                    r::move(mr, std::back_inserter(new_seed_ranges));
                }
                cur_range = std::move(new_seed_ranges);
            }
            cur_loc = rangemap.dest_name;
        }
        if (Range* ptr = std::get_if<Range>(&cur_range); ptr != nullptr) {
            return ptr->start;
        } else {
            const auto& ranges = std::get<std::vector<Range>>(cur_range);
            auto rng = ranges | v::transform([](auto&& r) { return r.start; });
            return r::min(rng);
        }
    }
};


int64_t part1(const std::vector<int64_t>& seeds, const LocMap& locmap) {
    auto mapped_seeds = seeds | v::transform([&locmap](auto&& seed) {
        return locmap.find_seed_location(seed);
    });
    return r::min(mapped_seeds);
}

int64_t part2(const std::vector<int64_t>& seeds, const LocMap& locmap) {
    auto mapped_seeds = seeds | v::chunk(2) | v::transform([&locmap](auto&& rng) {
        auto it = rng.begin();
        auto begin = *it;
        auto step = *(++it);
        return locmap.find_seed_range_location(Range{begin, begin + step});
    });
    return r::min(mapped_seeds);
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt" : "data.txt");
    auto iter = lines.begin();
    auto seeds = split_once((*iter++), ':').second | v::split(' ') | v::transform([](auto&& s) {
        int64_t n;
        std::from_chars(s.data(), s.data() + s.size(), n);
        return n;
    }) | r::to<std::vector>();
    auto locmap = LocMap::fromIter(iter, lines.end());
    std::printf("%lld %lld\n", part1(seeds, locmap), part2(seeds, locmap));
    return 0;
}