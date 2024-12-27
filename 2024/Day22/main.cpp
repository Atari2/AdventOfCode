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

constexpr size_t array_size = 20 * 20 * 20 * 20;

constexpr int64_t mi(int64_t v) {
    return v < 0 ? std::abs(v) + 10 : v;
}
constexpr size_t fi(int64_t a, int64_t b, int64_t c, int64_t d) {
    return (mi(a) * 20 * 20 * 20) + (mi(b) * 20 * 20) + (mi(c) * 20) + mi(d);
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

    auto changes = secrets | v::transform([](auto&& secret) {
        return v::zip(secret, secret | v::drop(1)) | v::transform([](auto&& p) {
            return (std::get<1>(p) % 10) - (std::get<0>(p) % 10);
        }) | r::to<std::vector>();
    });

    std::array<int16_t, array_size> bananas_sold{};
    std::array<int16_t, array_size> already_set{};
    for (auto&& [n, p] : v::zip(secrets, changes) | v::enumerate) {
        const auto& [secret, change] = p;
        for (auto&& [i, window] : change | v::slide(4) | v::enumerate) {
            auto idx = fi(window[0], window[1], window[2], window[3]);
            if (already_set[idx] != n) {
                bananas_sold[idx] += secret[i + 4] % 10;
                already_set[idx] = n;
            }
        }
    }
    auto part2 = r::max(bananas_sold);
    std::println("{} {}", part1, part2);
}