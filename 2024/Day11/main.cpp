#include <algorithm>
#include <charconv>
#include <fstream>
#include <ranges>
#include <string>
#include <string_view>
#include <variant>
#include <vector>
#include <cstdio>
#include <numeric>
#include <print>
#if __cpp_lib_generator	== 202207L
#include <generator>
#endif


namespace r = std::ranges;
namespace v = std::ranges::views;
using namespace std::string_view_literals;

constexpr bool SAMPLE_DATA = false;

std::string read_file(std::string_view filename) {
    std::ifstream file(filename.data());
    file.seekg(0, std::ios::end);
    size_t size = file.tellg();
    std::string contents{};
    contents.reserve(size);
    file.seekg(0, std::ios::beg);
    contents.assign((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
    return contents;
}

struct Stone {
    std::string value;
    size_t occurrences;

    Stone(std::string value, size_t occurrences = 1) {
        value.erase(value.begin(), std::find_if(value.begin(), value.end(), [](char c) { return c != '0'; }));
        if (value.size() != 0) this->value = std::move(value);
        else this->value = "0";
        this->occurrences = occurrences;
    }

    std::generator<Stone> blink() const {
        if (value == "0") {
            co_yield Stone("1", occurrences);
        } else if (size_t len = value.size(); len % 2 == 0) {
            co_yield Stone(value.substr(0, len / 2), occurrences);
            co_yield Stone(value.substr(len / 2), occurrences);
        } else {
            co_yield Stone(std::to_string(std::stoull(value) * 2024), occurrences);
        }
    }
};

int main() {
    auto data = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    auto stones = data | v::split(' ') | v::transform([](auto&& line) { return Stone{std::string(line.begin(), line.end())}; }) | r::to<std::vector>();
    size_t part1 = 0;
    for (size_t i = 0; i < 75; ++i) {
        if (i == 25) {
            part1 = r::fold_left(stones, 0, [](size_t acc, const auto& s) { return acc + s.occurrences; });
        }
        std::vector<Stone> new_stones{};
        for (const auto& stone : stones) {
            for (auto&& new_stone : stone.blink()) {
                if (auto it = r::find_if(new_stones, [&new_stone](const auto& s) { return s.value == new_stone.value; }); it != new_stones.end()) {
                    it->occurrences += new_stone.occurrences;
                } else {
                    new_stones.push_back(new_stone);
                }
            }
        }
        stones = std::move(new_stones);
    }
    size_t part2 = r::fold_left(stones, 0, [](size_t acc, const auto& s) { return acc + s.occurrences; });
    std::println("{} {}", part1, part2);
}
