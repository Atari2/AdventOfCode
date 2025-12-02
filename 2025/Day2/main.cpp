
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

std::string read_file(std::string_view filename) {
    std::ifstream file(filename.data());
    std::string data;
    file.seekg(0, std::ios::end);
    data.resize(file.tellg());
    file.seekg(0, std::ios::beg);
    file.read(&data[0], data.size());
    return data;
}

bool is_repeating_digits_twice(std::string_view n_str) {
    size_t k = n_str.size();
    if (k % 2 != 0) return false;
    size_t half_k = k / 2;
    std::string_view first_half = n_str.substr(0, half_k);
    std::string_view second_half = n_str.substr(half_k, half_k);
    return first_half == second_half;
}

bool is_repeating_digits_at_least_twice(std::string_view n_str) {
    size_t k = n_str.size();
    for (size_t size = 1; size <= k / 2; ++size) {
        if (k % size != 0) continue;
        auto pattern = n_str.substr(0, size);
        bool all_match = true;
        for (size_t start = size; start < k; start += size) {
            if (n_str.substr(start, size) != pattern) {
                all_match = false;
                break;
            }
        }
        if (all_match) return true;
    }
    return false;
}

int main() {
    auto data = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    auto ranges = data | v::split(',') | v::transform([](auto&& rng) {
        auto idx = r::find(rng, '-');
        size_t dash_pos = r::distance(rng.begin(), idx);
        int64_t n;
        std::from_chars(rng.data(), rng.data() + dash_pos, n);
        int64_t m;
        std::from_chars(rng.data() + dash_pos + 1, rng.data() + r::distance(rng), m);
        return std::make_pair(n, m);
    });
    int64_t p1 = 0;
    int64_t p2 = 0;
    for (auto [s, e] : ranges) {
        for (int64_t n = s; n <= e; ++n) {
            std::string n_str = std::to_string(n);
            if (is_repeating_digits_twice(n_str)) {
                p1 += n;
                p2 += n;
            } else if (is_repeating_digits_at_least_twice(n_str)) {
                p2 += n;
            }
        }
    }
    std::println("{} {}", p1, p2);
    return 0;
}