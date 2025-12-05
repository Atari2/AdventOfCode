
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

std::string_view trim(std::string_view sv) {
    size_t start = 0;
    while (start < sv.size() && std::isspace(static_cast<unsigned char>(sv[start]))) {
        ++start;
    }
    size_t end = sv.size();
    while (end > start && std::isspace(static_cast<unsigned char>(sv[end - 1]))) {
        --end;
    }
    return sv.substr(start, end - start);
}

struct InclusiveRange {
    int64_t start;
    int64_t end;

    bool contains(int64_t value) const {
        return value >= start && value <= end;
    }
    int64_t size() const {
        return end - start + 1;
    }

};

InclusiveRange parse_range(std::string_view sv) {
    size_t dash_pos = sv.find('-');
    int64_t start = 0;
    int64_t end = 0;
    std::from_chars(sv.data(), sv.data() + dash_pos, start);
    std::from_chars(sv.data() + dash_pos + 1, sv.data() + sv.size(), end);
    return {start, end};
}

std::vector<InclusiveRange> compress_ranges(std::vector<InclusiveRange>&& ranges) {
    if (ranges.empty()) {
        return {};
    }
    std::sort(ranges.begin(), ranges.end(),
        [](const InclusiveRange& a, const InclusiveRange& b) {
            return a.start < b.start;
        });
    std::vector<InclusiveRange> compressed;
    for (const auto& r : ranges) {
        bool was_compressed = false;
        for (auto& cr : compressed) {
            if (r.start <= cr.end + 1 && r.end >= cr.start - 1) {
                cr.start = std::min(cr.start, r.start);
                cr.end = std::max(cr.end, r.end);
                was_compressed = true;
                break;
            }
        }
        if (!was_compressed) {
            compressed.push_back(r);
        }
    }
    return compressed;
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    bool parsing_ranges = true;
    int64_t fresh_quantity = 0;
    int64_t total_fresh = 0;
    std::vector<InclusiveRange> fresh_ranges;
    for (const auto& line : lines) {
        std::string_view sv_line = trim(line);
        if (sv_line.empty()) {
            parsing_ranges = false;
            continue;
        }
        if (parsing_ranges) {
            fresh_ranges.push_back(parse_range(sv_line));
        } else {
            int64_t number = 0;
            std::from_chars(sv_line.data(), sv_line.data() + sv_line.size(), number);
            bool is_fresh = false;
            for (const auto& range : fresh_ranges) {
                if (range.contains(number)) {
                    fresh_quantity++;
                    break;
                }
            }
        }
    }
    auto compressed_ranges = compress_ranges(std::move(fresh_ranges));
    for (const auto& r : compressed_ranges) {
        total_fresh += r.size();
    }
    std::println("{} {}", fresh_quantity, total_fresh);
}