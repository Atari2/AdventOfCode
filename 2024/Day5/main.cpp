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
#include <cmath>

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

struct ordering_rule;

struct update {
    std::vector<int64_t> pages;

    update(r::range auto&& range) {
        auto r = range | v::split(',');
        for (const auto& el : r) {
            int64_t page;
            std::from_chars(el.data(), el.data() + el.size(), page);
            pages.push_back(page);
        }
    }

    int64_t center_page() const {
        return pages[pages.size() / 2];
    }

    void fix_update(const std::vector<ordering_rule>& rule);
};

struct ordering_rule {
    int64_t page_x;
    int64_t page_y;

    ordering_rule(r::range auto&& range) {
        auto r = range | v::split('|');
        auto it = r.begin();
        std::from_chars((*it).data(), (*it).data() + (*it).size(), page_x);
        ++it;
        std::from_chars((*it).data(), (*it).data() + (*it).size(), page_y);
    }

    bool is_update_valid(const update& u) const {
        auto page_x_idx = r::find(u.pages, page_x);
        auto page_y_idx = r::find(u.pages, page_y);
        if (page_x_idx == u.pages.end() || page_y_idx == u.pages.end()) {
            return true;
        }
        return std::distance(page_x_idx, page_y_idx) > 0;
    }
};

void update::fix_update(const std::vector<ordering_rule>& rules) {
    r::sort(pages, [&rules](const auto& lhs, const auto& rhs) {
        for (const auto& r : rules)   {
            if (r.page_x == lhs && r.page_y == rhs) {
                return false;
            }
            if (r.page_x == rhs && r.page_y == lhs) {
                return true;
            }
        } 
        throw std::runtime_error("Invalid ordering rule");
    });
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    std::vector<ordering_rule> rules;
    std::vector<update> updates;
    bool parsing_rules = true;
    for (const auto& line : lines) {
        if (line.empty()) {
            parsing_rules = false;
            continue;
        }
        if (parsing_rules) {
            rules.emplace_back(line);
        } else {
            updates.emplace_back(line);
        }
    }

    int64_t part1 = 0;
    int64_t part2 = 0;

    for (auto& u : updates) {
        if (r::all_of(rules, [&u](const auto& r) {
            return r.is_update_valid(u);
        })) {
            part1 += u.center_page();
        } else {
            u.fix_update(rules);
            part2 += u.center_page();
        }
    }

    std::println("{} {}", part1, part2);
}