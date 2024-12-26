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
#include <cinttypes>
#include <utility>
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

int64_t calculate_next(int64_t val) {
    val = ((val << 6) ^ val) & 0b111111111111111111111111;
    val = ((val >> 5) ^ val) & 0b111111111111111111111111;
    val = ((val << 11) ^ val) & 0b111111111111111111111111;
    return val;
}

std::vector<int64_t> save_nth(int64_t val, int64_t n) {
    std::vector<int64_t> res{val};
    for (int64_t i = 0; i < n; i++) {
        val = calculate_next(val);
        res.push_back(val);
    }
    return res;
}

static std::unordered_map<std::string, int64_t> count_cache{};

int64_t count_occurrences(const std::vector<std::unordered_map<std::string, int64_t>>& string_changes, const std::string& seq) {
    if (auto it = count_cache.find(seq); it != count_cache.end()) {
        return it->second;
    }
    auto val = r::fold_left(string_changes | v::transform([&](const auto& string_change) {
        if (auto it = string_change.find(seq); it != string_change.end()) {
            return it->second;
        }
        return int64_t{0};
    }), 0, std::plus{});
    count_cache[seq] = val;
    return val;
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv) | v::transform([](auto&& str) {
        return std::stoll(str);
    }) | r::to<std::vector>();

    auto secrets = lines | v::transform([](auto&& val) {
        return save_nth(val, 2000);
    }) | r::to<std::vector>();

    auto part1 = r::fold_left(secrets, 0, [](int64_t acc, const auto& secret) {
        return acc + secret.back();
    });

    std::vector<std::vector<std::string>> changes{};
    for (const auto& secret : secrets) {
        std::vector<std::string> change{};
        for (size_t i = 0; i < secret.size() - 1; ++i) {
            change.push_back(std::to_string((secret[i + 1] % 10) - (secret[i] % 10)));
        }
        changes.push_back(std::move(change));
    }
    std::vector<std::unordered_map<std::string, int64_t>> string_changes{};
    string_changes.reserve(changes.size());
    for (const auto& [secret, change] : v::zip(secrets, changes)) {
        std::unordered_map<std::string, int64_t> string_change{};
        string_change.reserve(change.size());
        int64_t idx = 0;
        for (auto&& seq : change | v::slide(4) | v::transform([](auto&& val) {
            return val | v::join | r::to<std::string>();
        })) {
            string_change.try_emplace(seq, secret[idx + 4] % 10);
            idx += 1;
        }
        string_changes.push_back(std::move(string_change));
    }

    int64_t current_max = 0;
    
    for (const auto& strc : string_changes) {
        for (const auto& seq : strc | v::keys) {
            current_max = std::max(current_max, count_occurrences(string_changes, seq));
        }
    }

    std::println("{} {}", part1, current_max);
}