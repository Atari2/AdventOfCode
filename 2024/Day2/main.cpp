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
#include <span>

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

enum class ReportType {
    Asc, Desc
};

bool check_valid_p1(r::range auto&& report) {
    auto latest_v = *report.begin();
    auto report_type = (*++report.begin()) > latest_v ? ReportType::Asc : ReportType::Desc;
    for (const auto& v : report | v::drop(1)) {
        auto diff = std::abs(v - latest_v);
        if (!(1 <= diff && diff <= 3)) {
            return false;
        }
        if (report_type == ReportType::Asc && v < latest_v) {
            return false;
        } else if (report_type == ReportType::Desc && v > latest_v) {
            return false;
        }
        latest_v = v;
    }
    return true;
}

bool check_valid_p2(std::span<const int32_t> report) {
    if (check_valid_p1(report)) {
        return true;
    } else {
        for (size_t i = 0; i < report.size(); i++) {
            // note: this method of skipping the i-th element is absolutely disgusting
            //       if this was C++26 we could use views::concat, but that doesn't exist in C++23 world
            //       this was the only way I could think of to skip the i-th element while using std::ranges and std::views.
            if (check_valid_p1(report | v::enumerate | v::filter([i](const auto& p){ return std::get<0>(p) != i; }) | v::transform([](const auto& p){ return std::get<1>(p); }))) {
                return true;
            }
        }
    }
    return false;
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    auto reports = lines | v::transform([](auto&& s) {
        return s | v::split(' ') | v::transform([](auto&& s) { 
            int32_t val;
            std::from_chars(s.data(), s.data() + s.size(), val);
            return val;
        }) | r::to<std::vector>();
    }) | r::to<std::vector>();

    auto p1 = r::fold_left(reports, 0, [](const auto& acc, const auto& report) {
        return acc + check_valid_p1(std::span{report});
    });

    auto p2 = r::fold_left(reports, 0, [](const auto& acc, const auto& report) {
        return acc + check_valid_p2(std::span{report});
    });

    std::println("{} {}", p1, p2);
}