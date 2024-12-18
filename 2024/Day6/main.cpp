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
#include <unordered_set>

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

std::pair<int64_t, int64_t> map_direction(char c) {
    switch (c) {
        case '^': return {-1, 0};
        case 'v': return {1, 0};
        case '<': return {0, -1};
        case '>': return {0, 1};
        default: throw std::invalid_argument("Invalid direction");
    }
}

char map_turn(char c) {
    switch (c) {
        case '^': return '>';
        case '>': return 'v';
        case 'v': return '<';
        case '<': return '^';
        default: throw std::invalid_argument("Invalid direction");
    }
}

bool pos_in_bounds(const std::pair<int64_t, int64_t>& new_pos, const std::vector<std::string>& data) {
    return new_pos.first >= 0 && new_pos.first < data.size() && new_pos.second >= 0 && new_pos.second < data[0].size();
}

template <>
struct std::hash<std::pair<std::pair<int64_t, int64_t>, char>> {

    constexpr static inline std::hash<int64_t> hasher{};
    constexpr static inline std::hash<char> char_hasher{};

    std::size_t operator()(const std::pair<std::pair<int64_t, int64_t>, char>& p) const {
        return hasher(p.first.first) ^ hasher(p.first.second) ^ char_hasher(p.second);
    }
};

int64_t part1(std::pair<int64_t, int64_t> current_pos, std::vector<std::string>& data) {
    auto current_dir = '^';
    while (true) {
        auto direction = map_direction(current_dir);
        data[current_pos.first][current_pos.second] = 'X';
        auto new_pos = std::make_pair(current_pos.first + direction.first, current_pos.second + direction.second);
        if (!pos_in_bounds(new_pos, data)) {
            break;
        }
        if (data[new_pos.first][new_pos.second] != '#') {
            current_pos = new_pos;
        } else {
            current_dir = map_turn(current_dir);
        }
        data[current_pos.first][current_pos.second] = current_dir;
    }
    return r::fold_left(data | v::join, 0, [](int64_t acc, char c) {
        return acc + (c == 'X');
    });
}

int64_t part2(std::pair<int64_t, int64_t> starting_pos, std::vector<std::string>& data) {
    const auto obstacles_possible_pos = [&]() {
        std::vector<std::pair<int64_t, int64_t>> res;
        for (int64_t i = 0; i < data.size(); ++i) {
            for (int64_t j = 0; j < data[i].size(); ++j) {
                if (data[i][j] == 'X') {
                    res.push_back(std::make_pair(i, j));
                }
            }
        }
        return res;
    }();
    int64_t loops = 0;
    std::unordered_set<std::pair<std::pair<int64_t, int64_t>, char>> visited_stack;
    for (const auto& [obstacle_pos_x, obstacle_pos_y] : obstacles_possible_pos) {
        auto current_pos = starting_pos;
        auto current_dir = '^';
        data[obstacle_pos_x][obstacle_pos_y] = '#';
        visited_stack.clear();
        while (true) {
            if (auto&& [_, inserted] = visited_stack.insert({current_pos, current_dir}); !inserted) {
                loops++;
                break;
            }
            auto [dx, dy] = map_direction(current_dir);
            auto new_pos = std::make_pair(current_pos.first + dx, current_pos.second + dy);
            if (!pos_in_bounds(new_pos, data)) {
                break;
            }
            if (data[new_pos.first][new_pos.second] != '#') {
                current_pos = new_pos;
            } else {
                current_dir = map_turn(current_dir);
            }
        }
        data[obstacle_pos_x][obstacle_pos_y] = 'X';
    }
    return loops;
}

int main() {
    auto data = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);

    const auto starting_pos = [&]() {
        for (int64_t i = 0; i < data.size(); ++i) {
            for (int64_t j = 0; j < data[i].size(); ++j) {
                if (data[i][j] == '^') {
                    return std::make_pair(i, j);
                }
            }
        }
        throw std::invalid_argument("No starting position found");
    }();

    auto part1res = part1(starting_pos, data);
    auto part2res = part2(starting_pos, data);

    std::println("{} {}", part1res, part2res);

}