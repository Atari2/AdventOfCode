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
#include <queue>
#include <utility>
#if __cpp_lib_generator	== 202207L
#include <generator>
#endif

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

struct point {
    int64_t x;
    int64_t y;

    point& operator+=(point other) {
        x += other.x;
        y += other.y;
        return *this;
    }
    point operator+(point other) const {
        return {x + other.x, y + other.y};
    }
    point& operator-=(point other) {
        x -= other.x;
        y -= other.y;
        return *this;
    }
    point operator-(point other) const {
        return {x - other.x, y - other.y};
    }
    point operator*(int64_t scale) const {
        return {x * scale, y * scale};
    }
    bool operator==(point other) const {
        return x == other.x && y == other.y;
    }
};


template <typename Container>
struct matrix {
    Container data;

    const auto& operator[](point p) const {
        return data[p.x][p.y];
    }
    auto& operator[](point p) {
        return data[p.x][p.y];
    }

    point find(auto c) const {
        for (int64_t x = 0; x < data.size(); x++) {
            for (int64_t y = 0; y < data[x].size(); y++) {
                if (data[x][y] == c) {
                    return {x, y};
                }
            }
        }
        return {-1, -1};
    }

#if __cpp_lib_generator	== 202207L
    std::generator<point> find_all(auto c) const {
        for (int64_t x = 0; x < data.size(); x++) {
            for (int64_t y = 0; y < data[x].size(); y++) {
                if (data[x][y] == c) {
                    co_yield {x, y};
                }
            }
        }
    }
#else
    std::vector<point> find_all(auto c) const {
        std::vector<point> result{};
        for (int64_t x = 0; x < data.size(); x++) {
            for (int64_t y = 0; y < data[x].size(); y++) {
                if (data[x][y] == c) {
                    result.emplace_back(x, y);
                }
            }
        }
        return result;
    }
#endif
};

struct box {
    point l;
    point r;
};

int64_t part1(matrix<std::span<std::string>>& warehouse, r::range auto&& commands) {
    auto robot = warehouse.find('@');

    auto move_box = [&](this const auto& move_box, point box_position, point direction) -> bool {
        if (warehouse[box_position + direction] == '.') {
            warehouse[box_position] = '.';
            box_position += direction;
            warehouse[box_position] = 'O';
            return true;
        } else if (warehouse[box_position + direction] == 'O') {
            if (move_box(box_position + direction, direction)) {
                warehouse[box_position] = '.';
                box_position += direction;
                warehouse[box_position] = 'O';
                return true;
            } else {
                return false;
            }
        } else {
            return false;
        }
    };

    auto move = [&](point direction) {
        auto new_position = robot + direction;
        if (auto cell = warehouse[new_position]; cell == '.') {
            warehouse[robot] = '.';
            robot = new_position;
            warehouse[robot] = '@';
        } else if (cell == 'O') {
            if (move_box(new_position, direction)) {
                warehouse[robot] = '.';
                robot = new_position;
                warehouse[robot] = '@';
            }
        }
    };

    for (auto command : commands) {
        switch (command) {
            case '<': move({0, -1}); break;
            case '>': move({0, 1}); break;
            case '^': move({-1, 0}); break;
            case 'v': move({1, 0}); break;
        }
    }

    int64_t tot = 0;
    for (auto [x, y] : warehouse.find_all('O')) {
        tot += (x * 100) + y;
    }
    return tot;

}

int64_t part2(matrix<std::span<std::string>>& warehouse, r::range auto&& commands) {
    matrix<std::vector<std::string>> wider_warehouse{};
    wider_warehouse.data.resize(warehouse.data.size());
    for (int64_t x = 0; x < warehouse.data.size(); x++) {
        wider_warehouse.data[x].resize(warehouse.data[x].size() * 2);
        for (int64_t y = 0, j = 0; y < warehouse.data[x].size(); y++, j += 2) {
            switch (warehouse[{x, y}]) {
                case '#': wider_warehouse[{x, j}] = '#'; wider_warehouse[{x, j + 1}] = '#'; break;
                case '.': wider_warehouse[{x, j}] = '.'; wider_warehouse[{x, j + 1}] = '.'; break;
                case 'O': wider_warehouse[{x, j}] = '['; wider_warehouse[{x, j + 1}] = ']'; break;
                case '@': wider_warehouse[{x, j}] = '@'; wider_warehouse[{x, j + 1}] = '.'; break;
            }
        }
    }
    auto robot = wider_warehouse.find('@');

    auto move_box_horizontal = [&](this const auto& move_box_horizontal, box box_positions, point direction) -> bool {
        auto [l, r] = box_positions;
        if ((direction == point{0, 1} && wider_warehouse[r + direction] == '.') || 
            (direction == point{0, -1} && wider_warehouse[l + direction] == '.')) { 
            wider_warehouse[l] = '.';
            wider_warehouse[r] = '.';
            l += direction;
            r += direction;
            wider_warehouse[l] = '[';
            wider_warehouse[r] = ']';
            return true;
        } else if ((direction == point{0, 1} && wider_warehouse[r + direction] == '[') || 
                   (direction == point{0, -1} && wider_warehouse[l + direction] == ']')) {
            if (move_box_horizontal({l + (direction * 2), r + (direction * 2)}, direction)) {
                wider_warehouse[l] = '.';
                wider_warehouse[r] = '.';
                l += direction;
                r += direction;
                wider_warehouse[l] = '[';
                wider_warehouse[r] = ']';
                return true;
            } else {
                return false;
            }
        } else {
            return false;
        }
    };

    auto move_box_vertical = [&](this const auto& move_box_vertical, box box_positions, point direction) -> bool {
        auto [l, r] = box_positions;
        if (wider_warehouse[l + direction] == '.' && wider_warehouse[r + direction] == '.') {
            wider_warehouse[l] = '.';
            wider_warehouse[r] = '.';
            l += direction;
            r += direction;
            wider_warehouse[l] = '[';
            wider_warehouse[r] = ']';
            return true;
        } else if (wider_warehouse[l + direction] == '[') {
            if (move_box_vertical({l + direction, r + direction}, direction)) {
                wider_warehouse[l] = '.';
                wider_warehouse[r] = '.';
                l += direction;
                r += direction;
                wider_warehouse[l] = '[';
                wider_warehouse[r] = ']';
                return true;
            } else {
                return false;
            }
        } else if (wider_warehouse[l + direction] == ']' && wider_warehouse[r + direction] == '[') {
            auto box1 = box{l + direction + point{0, -1}, l + direction};
            auto box2 = box{r + direction, r + direction + point{0, 1}};
            auto saved_warehouse = wider_warehouse;
            if (move_box_vertical(box1, direction) && move_box_vertical(box2, direction)) {
                wider_warehouse[l] = '.';
                wider_warehouse[r] = '.';
                l += direction;
                r += direction;
                wider_warehouse[l] = '[';
                wider_warehouse[r] = ']';
                return true;
            } else {
                wider_warehouse = saved_warehouse;
                return false;
            }
        } else if (wider_warehouse[l + direction] == ']' && wider_warehouse[r + direction] == '.') {
            auto box1 = box{l + direction + point{0, -1}, l + direction};
            if (move_box_vertical(box1, direction)) {
                wider_warehouse[l] = '.';
                wider_warehouse[r] = '.';
                l += direction;
                r += direction;
                wider_warehouse[l] = '[';
                wider_warehouse[r] = ']';
                return true;
            } else {
                return false;
            }
        } else if (wider_warehouse[r + direction] == '[' && wider_warehouse[l + direction] == '.') {
            auto box2 = box{r + direction, r + direction + point{0, 1}};
            if (move_box_vertical(box2, direction)) {
                wider_warehouse[l] = '.';
                wider_warehouse[r] = '.';
                l += direction;
                r += direction;
                wider_warehouse[l] = '[';
                wider_warehouse[r] = ']';
                return true;
            } else {
                return false;
            }
        } else {
            return false;
        }
    };

    auto move = [&](point direction) {
        auto new_position = robot + direction;
        if (auto cell = wider_warehouse[new_position]; cell == '.') {
            wider_warehouse[robot] = '.';
            robot = new_position;
            wider_warehouse[robot] = '@';
        } else if (cell == '[' or cell == ']') {
            if (direction == point{0, 1} || direction == point{0, -1}) {
                auto boxes = cell == '[' ? box{new_position, new_position + point{0, 1}} : box{new_position + point{0, -1}, new_position};
                if (move_box_horizontal(boxes, direction)) {
                    wider_warehouse[robot] = '.';
                    robot = new_position;
                    wider_warehouse[robot] = '@';
                }
            } else {
                auto boxes = cell == '[' ? box{new_position, new_position + point{0, 1}} : box{new_position + point{0, -1}, new_position};
                if (move_box_vertical(boxes, direction)) {
                    wider_warehouse[robot] = '.';
                    robot = new_position;
                    wider_warehouse[robot] = '@';
                }
            }
        }
    };

    for (auto command : commands) {
        switch (command) {
            case '<': move({0, -1}); break;
            case '>': move({0, 1}); break;
            case '^': move({-1, 0}); break;
            case 'v': move({1, 0}); break;
        }
    }

    int64_t tot = 0;
    for (auto [x, y] : wider_warehouse.find_all('[')) {
        tot += (x * 100) + y;
    }
    return tot;
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    auto spaceidx = r::find(lines, ""sv);
    auto warehouse = matrix{std::span{lines.begin(), spaceidx}};
    auto commands = std::span{spaceidx + 1, lines.end()} | v::join;
    std::println("{} {}", part1(warehouse, commands), part2(warehouse, commands));
}