
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

int64_t part1(const std::vector<std::string>& lines) {
    int64_t dial_position = 50;
    int64_t psw = 0;
    for (const auto& line : lines) {
        char direction = line[0];
        int64_t amount;
        std::from_chars(line.data() + 1, line.data() + line.size(), amount);
        if (direction == 'R') {
            dial_position = (dial_position + amount) % 100;
        } else if (direction == 'L') {
            dial_position = (dial_position - amount) % 100;
        }
        // C++ doesn't do euclidean mod for negative numbers
        // fix it
        if (dial_position < 0) dial_position += 100;
        if (dial_position == 0) {
            psw += 1;
        }
    }
    return psw;
}

int64_t part2(const std::vector<std::string>& lines) {
    int64_t dial_position = 50;
    int64_t psw = 0;
    for (const auto& line : lines) {
        char direction = line[0];
        int64_t amount;
        std::from_chars(line.data() + 1, line.data() + line.size(), amount);
        int64_t turns = amount / 100;
        psw += turns;
        int64_t remaining_amount = amount % 100;
        if (direction == 'R') {
            int64_t dial_temp = dial_position + remaining_amount;
            if (dial_temp >= 100) {
                psw += 1;
            }
            dial_position = dial_temp % 100;
        } else if (direction == 'L') {
            int64_t dial_temp = dial_position - remaining_amount;
            if (dial_temp <= 0 && dial_position > 0) {
                psw += 1;
            }
            dial_position = dial_temp % 100;
        }
        // C++ doesn't do euclidean mod for negative numbers
        // fix it.
        if (dial_position < 0) dial_position += 100;
    }
    return psw;
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    std::println("{} {}", part1(lines), part2(lines));
}