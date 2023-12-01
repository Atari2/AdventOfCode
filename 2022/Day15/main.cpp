// compile with: cl /nologo /O2 /EHsc /std:c++latest main.cpp
#include <version>
#ifndef _MSC_VER
#error "This code requires an MSVC compiler"
#else
#if _MSC_VER < 1935 || !defined(_WIN64) || !_HAS_CXX23 || __cpp_lib_ranges != 202207L
#error "This code is for x64 MSVC 19.35+ only and requires C++23 features"
#endif
#endif
#include <fstream>
#include <iostream>
#include <cstdio>
#include <ranges>
#include <vector>
#include <string_view>
#include <string>
#include <utility>
#include <cstdlib>
#include <optional>
#include <algorithm>
#include <array>
#include <thread>
#include <future>

constexpr bool SAMPLE_DATA = false;

namespace r = std::ranges;
namespace v = std::ranges::views;

std::vector<std::string> read_file(std::string_view filename) {
    std::ifstream file(filename.data());
    std::vector<std::string> lines;
    std::string line;
    while (std::getline(file, line)) {
        lines.push_back(line);
    }
    return lines;
}

struct Range {
    int s;
    int e;

    bool intersect(const Range& other) const {
        if (s <= other.s && other.s <= e) {
            return true;
        } else if (s <= other.e && other.e <= e) {
            return true;
        } else if (other.s <= s && s <= other.e) {
            return true;
        } else if (other.s <= e && e <= other.e) {
            return true;
        }
        return false;
    }
    static Range merge(const Range& a, const Range& b) {
        return Range{std::min(a.s, b.s), std::max(a.e, b.e)};
    }
};

struct Point {
    int x;
    int y;
};

int md(const Point& a, const Point& b) {
    return std::abs(a.x - b.x) + std::abs(a.y - b.y);
}

struct Sensor : public Point {
    Point beacon;
    std::pair<Point, Point> area;
    Sensor(int sx, int sy, Point b) : Point{sx, sy}, beacon{b} {
        auto dist = md(*this, beacon);
        area = std::make_pair(Point{sx, sy - dist}, Point{sx, sy + dist});
    }

    std::optional<Range> intersect_row(int row) const {
        int diff = 0;
        int vpx = 0;
        if (y <= row && row <= area.second.y) {
            diff = area.second.y - row;
            vpx = area.second.x;
        } else if (area.first.y <= row && row <= y) {
            diff = area.first.y - row;
            vpx = area.first.x;
        } else {
            return std::nullopt;
        }
        float occupies = (diff * 2) + 1;
        int x1 = vpx - std::floor(occupies / 2.0);
        int x2 = vpx + std::floor(occupies / 2.0);
        return Range{x1 < x2 ? x1 : x2, x1 > x2 ? x1 : x2};
    }
};

std::pair<std::vector<Range>, int> _reduce_ranges(std::vector<Range>&& points) {
    thread_local std::array<bool, 256> merged_indexes{};
    std::memset(merged_indexes.data(), false, sizeof(bool) * merged_indexes.size());
    std::vector<Range> reduced;
    reduced.reserve(points.size());
    int reduced_by = 0;
    for (int i = 0; i < points.size(); i++) {
        if (merged_indexes[i])
            continue;
        const auto& r1 = points[i];
        std::optional<Range> merged_range{};
        for (int j = i + 1; j < points.size(); j++) {
            if (merged_indexes[j])
                continue;
            const auto& r2 = points[j];
            if (r1.intersect(r2)) {
                merged_range = Range::merge(r1, r2);
                merged_indexes[j] = true;
                merged_indexes[i] = true;
                reduced_by++;
                break;
            }
        }
        if (merged_range.has_value()) {
            reduced.push_back(merged_range.value());
        } else {
            reduced.push_back(r1);
        }
    }
    return std::make_pair(std::move(reduced), reduced_by);
}

std::vector<Range> reduce_ranges(std::vector<Range> ranges) {
    r::sort(ranges, [](const auto& a, const auto& b) {
        return a.s < b.s;
    });
    auto tp = _reduce_ranges(std::move(ranges));
    while (tp.second > 0) {
        tp = _reduce_ranges(std::move(tp.first));
    }
    return tp.first;
}

std::vector<Range> create_intersect_ranges(const std::vector<Sensor>& sensors, int row) {
    std::vector<Range> ranges;
    for (const auto& sensor : sensors) {
        if (auto range = sensor.intersect_row(row); range.has_value()) {
            ranges.push_back(range.value());
        }
    }
    return reduce_ranges(std::move(ranges));
}

size_t part1(const std::vector<Sensor>& sensors) {
    auto ranges = create_intersect_ranges(sensors, SAMPLE_DATA ? 10 : 2'000'000);
    auto min_x = r::min(ranges, {}, &Range::s).s;
    auto max_x = r::max(ranges, {}, &Range::e).e;
    return std::abs(min_x) + (max_x);
}

size_t part2(const std::vector<Sensor>& sensors) {
    constexpr auto max_row = SAMPLE_DATA ? 20 : 4'000'000;
    auto n_threads = std::thread::hardware_concurrency();
    auto row_per_thread = max_row / n_threads;
    using ret = std::pair<size_t, int>;
    using ft = std::future<ret>;
    std::vector<ft> threads;
    threads.reserve(n_threads);
    constexpr size_t max = 0;
    for (int i = 0; i < max_row; i += row_per_thread) {
        threads.emplace_back(std::async(std::launch::async, [&sensors, i, row_per_thread]() -> ret {
            for (int row = i; row < i+row_per_thread; row++) {
                auto ranges = create_intersect_ranges(sensors, row);
                if (ranges.size() > 1) {
                    return {static_cast<size_t>(ranges[0].e + 1) * 4'000'000ull + row, row};
                }
            }
            return {0, max_row};
        }));
    }
    auto values = v::transform(threads, &ft::get) | r::to<std::vector<ret>>();
    return r::min(values, {}, &ret::second).first;
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt" : "data.txt");
    std::vector<Sensor> sensors;
    for (const auto& line : lines) {
        int x, y, bx, by;
        sscanf(line.data(), "Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d", &x, &y, &bx, &by);
        sensors.emplace_back(x, y, Point{bx, by});
    }
    std::cout << part1(sensors) << ' ' << part2(sensors) << '\n';
}