
#include <algorithm>
#include <charconv>
#include <fstream>
#include <ranges>
#include <string>
#include <string_view>
#include <unordered_map>
#include <set>
#include <unordered_set>
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
using ss = std::set<std::string_view>;

using cycle = std::tuple<std::string_view, std::string_view, std::string_view>;

template <>
struct std::hash<cycle> {
    constexpr static inline std::hash<std::string_view> hasher{};
    std::size_t operator()(const cycle& c) const noexcept {
        return hasher(std::get<0>(c)) ^ hasher(std::get<1>(c)) ^ hasher(std::get<2>(c));
    }
};

int64_t find_cycles(const std::unordered_map<std::string_view, ss>& graph) {
    std::array<std::string_view, 3> temp_stack{};
    auto dfs_cycle = [&](
        this const auto& dfs_cycle,
        std::string_view node, 
        std::string_view start, 
        std::unordered_set<std::string_view>& visited, 
        std::vector<std::string_view>& stack, 
        std::unordered_set<cycle>& cycles) -> void {
            visited.insert(node);
            stack.push_back(node);

            if (auto it = graph.find(node); it != graph.end()) {
                for (const auto& neighbor : it->second) {
                    if (neighbor == start && stack.size() == 3 && r::any_of(stack, [](auto&& s) { return s[0] == 't'; })) {
                        temp_stack[0] = stack[0];
                        temp_stack[1] = stack[1];
                        temp_stack[2] = stack[2];
                        r::sort(temp_stack);
                        cycles.emplace(temp_stack[0], temp_stack[1], temp_stack[2]);
                    } else if (!visited.contains(neighbor) && stack.size() < 3) {
                        dfs_cycle(neighbor, start, visited, stack, cycles);
                    }
                }
            }

            stack.pop_back();
            visited.erase(node);
    };

    std::unordered_set<cycle> cycles{};
    for (const auto& node : graph | v::keys) {
        std::unordered_set<std::string_view> visited{};
        std::vector<std::string_view> stack{};
        dfs_cycle(node, node, visited, stack, cycles);
    }
    return cycles.size();
}

std::optional<ss> bron_kerbosch1(const std::unordered_map<std::string_view, ss>& computers, std::vector<ss>& cliques, ss&& r, ss&& p, ss&& x)  {
    if (p.empty() && x.empty()) {
        return r;
    }
    auto p_copy = p;
    for (const auto& v : p_copy) {
        auto rv = ss{r};
        rv.insert(v);
        ss pi{};
        r::set_intersection(p, computers.at(v), std::inserter(pi, pi.end()));
        ss xi{};
        r::set_intersection(x, computers.at(v), std::inserter(xi, xi.end()));
        auto ret = bron_kerbosch1(computers, cliques, std::move(rv), std::move(pi), std::move(xi));
        if (ret.has_value()) {
            cliques.push_back(std::move(ret.value()));
        }
        p.erase(v);
        x.insert(v);
    }
    return std::nullopt;
};



int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    auto computers = lines | v::transform([](auto&& line) {
        return line | v::split('-');
    }) | v::join | v::transform([](auto&& str) {
        return std::make_pair(std::string_view{str}, ss{});
    }) | r::to<std::unordered_map>();
    for (const auto& line : lines) {
        auto r = line | v::split('-') | v::transform([](auto&& str) {
            return std::string_view{str};
        });
        auto it = r.begin();
        auto from = *it++;
        auto to = *it++;
        computers[from].insert(to);
        computers[to].insert(from);
    }

    auto part1 = find_cycles(computers);

    std::vector<ss> cliques{};
    bron_kerbosch1(computers, cliques, {}, computers | v::keys | r::to<ss>(), {});
    auto longest_clique = r::max(cliques, {}, &ss::size) | v::join_with(',') | r::to<std::string>();
    std::println("{} {}", part1, longest_clique);
    return 0;
}