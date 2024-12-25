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

int64_t count_occurrences(const std::vector<std::vector<int64_t>>& secrets, const std::vector<std::string>& string_changes, const std::string& seq) {
    if (auto it = count_cache.find(seq); it != count_cache.end()) {
        return it->second;
    }
    int64_t count = 0;
    for (auto&& [i, change] : string_changes | v::enumerate) {
        int64_t idx = 0;
        while ((idx = change.find(seq, idx)) != std::string::npos) {
            if (change[idx - 1] == '-') {
                idx += 1;
                continue;
            }
            std::string_view changeview{change};
            count += secrets[i][idx + seq.size() - r::count(changeview.substr(0, idx + seq.size()), '-')] % 10;
            break;
        }
    }
    count_cache[seq] = count;
    return count;
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

    std::vector<std::vector<int64_t>> changes{};
    for (const auto& secret : secrets) {
        std::vector<int64_t> change{};
        for (size_t i = 0; i < secret.size() - 1; ++i) {
            change.push_back((secret[i + 1] % 10) - (secret[i] % 10));
        }
        changes.push_back(std::move(change));
    }
    auto string_changes = changes | v::transform([](const auto& change) {
        return change | v::transform([](auto&& val) {
            return std::to_string(val);
        }) | v::join | r::to<std::string>();
    }) | r::to<std::vector>();

    int64_t current_max = 0;
    for (const auto& change : changes) {
        std::span change_span{change};
        for (size_t i = 0; i < change.size() - 4; ++i) {
            auto seq = change_span.subspan(i, 4) | v::transform([](auto&& val) {
                return std::to_string(val);
            }) | v::join | r::to<std::string>();
            auto pr = count_occurrences(secrets, string_changes, seq);
            current_max = std::max(current_max, pr);
        }
    }

    std::println("{} {}", part1, current_max);
}