// compile with: cl /nologo /O2 /EHsc /std:c++latest main.cpp
// most of this is just me playing around with C++23 ranges and views
#include <version>
#ifndef _MSC_VER
#error "This code requires an MSVC compiler"
#else
#if _MSC_VER < 1935 || !defined(_WIN64) || !_HAS_CXX23 || __cpp_lib_ranges < 202207L
#error "This code is for x64 MSVC 19.35+ only and requires C++23 features"
#endif
#endif

#include <algorithm>
#include <charconv>
#include <fstream>
#include <ranges>
#include <string>
#include <string_view>
#include <vector>
#include <unordered_map>
#include <cstdio>

constexpr bool SAMPLE_DATA = false;

namespace r = std::ranges;
namespace v = std::ranges::views;
using namespace std::string_view_literals;

std::vector<std::string> read_file(std::string_view filename) {
    std::ifstream file(filename.data());
    std::vector<std::string> lines;
    std::string line;
    while (std::getline(file, line)) {
        lines.push_back(line);
    }
    return lines;
}

auto strip_view(std::string_view line) {
    auto first = line.find_first_not_of(' ');
    auto last = line.find_last_not_of(' ');
    return line.substr(first, last - first + 1);
}

using CubeSets = std::vector<std::pair<size_t, std::string_view>>;
using BagType = std::unordered_map<std::string_view, size_t>;

class Game {
    size_t m_id;
    CubeSets m_cubesubsets;
    const BagType& s_bag;

    public:
    Game(size_t id, CubeSets&& cubesubsets, const BagType& bag) : m_id(id), m_cubesubsets(std::forward<CubeSets>(cubesubsets)), s_bag(bag) {}
    static Game fromLine(std::string_view line, const BagType& bag) {
        size_t id = 0;
        int read_until = 0;
        ::sscanf_s(line.data(), "Game %zu: %n", &id, &read_until); 
        std::string_view cubesets = line.substr(read_until);
        auto v = cubesets | v::split(";"sv) | v::transform([](auto&& cubeset) {
            return cubeset | v::split(","sv) | v::transform([](auto&& cube) {
                auto cube_view = strip_view(std::string_view{cube});
                size_t space_idx = cube_view.find(' ');
                size_t qty = 0;
                std::from_chars(cube_view.data(), cube_view.data() + space_idx, qty);
                return std::make_pair(qty, cube_view.substr(space_idx + 1));
            });
        }) | v::join | r::to<std::vector>();
        return Game{id, std::move(v), bag};
    }
    bool is_possible() const {
        for (const auto& [qty, color] : m_cubesubsets) {
            auto it = s_bag.find(color);
            if (it == s_bag.end() || it->second < qty) {
                return false;
            }
        }
        return true;
    }
    size_t min_bag_power() const {
        BagType gbag{};
        for (const auto& [qty, color] : m_cubesubsets) {
            auto& val = gbag[color];
            val = std::max(val, qty);
        }
        return r::fold_left(gbag | v::transform(&BagType::value_type::second), 1, std::multiplies<>{});
    }
    size_t id () const { return m_id; }
};

int main() {
    const BagType bag{
        { "red"sv, 12 },
        { "green"sv, 13 },
        { "blue"sv, 14 }
    };
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt" : "data.txt");
    auto games = lines | v::transform([&bag](auto&& line) { return Game::fromLine(line, bag); }) | r::to<std::vector>();
    auto totalp1 = r::fold_left(games | v::filter(&Game::is_possible) | v::transform(&Game::id), 0, std::plus<>{});
    auto totalp2 = r::fold_left(games | v::transform(&Game::min_bag_power), 0, std::plus<>{});
    std::printf("%zu %zu", totalp1, totalp2);
    return 0;
}