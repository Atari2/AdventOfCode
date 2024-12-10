#include <algorithm>
#include <charconv>
#include <fstream>
#include <ranges>
#include <string>
#include <string_view>
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

std::vector<std::string> read_file(std::string_view filename) {
    std::ifstream file(filename.data());
    std::vector<std::string> lines;
    std::string line;
    while (std::getline(file, line)) {
        lines.push_back(line);
    }
    return lines;
}
using point = std::pair<int64_t, int64_t>;
template <typename T>
using matrix = std::vector<std::vector<T>>;
constexpr const std::array<point, 4> DIRECTIONS = {{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}};
constexpr const uint8_t MAX_HEIGHT = 9;
#if __cpp_lib_generator	== 202207L
std::generator<point> generate_neighbours(int64_t x, int64_t y, const matrix<uint8_t>& data) {
    for (const auto& [dx, dy] : DIRECTIONS) {
        if (x + dx >= 0 && x + dx < data.size() && y + dy >= 0 && y + dy < data[0].size())
            co_yield point{x + dx, y + dy};
    }
}
#else
std::vector<point> generate_neighbours(int64_t x, int64_t y, const matrix<uint8_t>& data) {
    std::vector<point> neighbours;
    for (const auto& [dx, dy] : DIRECTIONS) {
        if (x + dx >= 0 && x + dx < data.size() && y + dy >= 0 && y + dy < data[0].size())
            neighbours.push_back({x + dx, y + dy});
    }
    return neighbours;
}
#endif

struct Node {
    uint8_t value;
    std::vector<const Node*> neighbours;
    point pos;

    Node(int64_t x, int64_t y, const matrix<uint8_t>& data) {
        pos = {x, y};
        value = data[x][y];
        neighbours = {};
    }

    void populate_neighbours(const matrix<Node>& nodes, const matrix<uint8_t>& data) {
        if (value != MAX_HEIGHT) {
            for (const auto& [nx, ny] : generate_neighbours(pos.first, pos.second, data)) {
                if (nodes[nx][ny].value == value + 1) {
                    neighbours.push_back(&nodes[nx][ny]);
                }
            }
        }
    }
};

int64_t find_all_paths(const Node* node, const Node* ending_node, std::vector<const Node*>& visited, int64_t depth = 0) {
    if (node == ending_node) {
        return 1;
    }
    visited.push_back(node);
    int64_t paths = 0;
    for (const auto* neighbour : node->neighbours) {
        if (r::find(visited, neighbour) == visited.end()) {
            paths += find_all_paths(neighbour, ending_node, visited, depth + 1);
        }
    }
    visited.pop_back();
    return paths;
}


int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    auto data = lines | v::transform([](auto&& line) {
        return line | v::transform([](char c) -> uint8_t { return c - '0'; }) | r::to<std::vector>();
    }) | r::to<std::vector>();

    auto nodes = data | v::enumerate | v::transform([&data](auto&& p) {
        auto&& [x, row] = p;
        return row | v::enumerate | v::transform([&data, x](auto&& p) {
            auto&& [y, value] = p;
            return Node{x, y, data};
        }) | r::to<std::vector>();
    }) | r::to<std::vector>();

    for (auto& row : nodes) {
        for (auto& node : row) {
            node.populate_neighbours(nodes, data);
        }
    }

    auto starting_nodes = nodes | v::join | v::filter([](const auto& node) { return node.value == 0; }) | v::transform([](const auto& node) { return &node; });
    auto ending_nodes = nodes | v::join | v::filter([](const auto& node) { return node.value == MAX_HEIGHT; }) | v::transform([](const auto& node) { return &node; });

    int64_t tot_score = 0;
    int64_t tot_rating = 0;
    std::vector<const Node*> visited{};
    for (const auto* start : starting_nodes) {
        for (const auto* end : ending_nodes) {
            auto rating = find_all_paths(start, end, visited);
            tot_score += rating != 0 ? 1 : 0;
            tot_rating += rating;
            visited.clear();
        }
    }

    std::println("{} {}", tot_score, tot_rating);
}