// compile with: cl /nologo /O2 /EHsc /std:c++latest main.cpp
#include <version>
#ifndef _MSC_VER
#error "This code requires an MSVC compiler"
#else
#if _MSC_VER < 1935 || !defined(_WIN64) || !_HAS_CXX23 || __cpp_lib_ranges != 202207L
#error "This code is for x64 MSVC 19.35+ only and requires C++23 features"
#endif
#endif
#include <unordered_set>
#include <vector>
#include <string>
#include <string_view>
#include <iostream>
#include <fstream>
#include <ranges>
#include <span>
#include <algorithm>
#include <charconv>

std::vector<std::string> read_file(std::string_view filename)
{
    std::ifstream file(filename.data());
    std::vector<std::string> lines;
    std::string line;
    while (std::getline(file, line))
    {
        lines.push_back(line);
    }
    return lines;
}

using Point = std::pair<int, int>;
namespace v = std::ranges::views;
namespace r = std::ranges;
using namespace std::string_view_literals;
using cmatrix = std::vector<std::vector<char>>;

template <>
struct std::hash<Point>
{
    std::size_t operator()(const Point &p) const noexcept
    {
        static_assert(sizeof(int) * 2 == sizeof(size_t));
        return (static_cast<size_t>(p.first) << (sizeof(int) * CHAR_BIT)) | static_cast<size_t>(p.second);
    }
};

struct Path
{
    std::vector<Point> m_path;

    static constexpr auto to_view = [](auto &&subr)
    { return std::string_view{subr.begin(), subr.end()}; };
    static constexpr auto to_int = [](auto &&subr)
    {
        int i;
        const char *ptr = &*subr.begin();
        auto sz = r::distance(subr);
        std::from_chars(ptr, ptr + sz, i);
        return i;
    };

    Path(std::string_view path)
    {
        for (const auto w : v::split(path, " -> "sv) | v::transform(to_view))
        {
            auto p = v::split(w, ","sv) | v::transform(to_int);
            m_path.push_back({*p.begin(), *std::next(p.begin())});
        };
    }

    void normalize(int min_x)
    {
        for (auto &point : m_path)
        {
            point.first -= min_x;
        }
    }

    int min_x() const
    {
        return r::min_element(m_path, {}, &Point::first)->first;
    }

    int max_x() const
    {
        return r::max_element(m_path, {}, &Point::first)->first;
    }

    int min_y() const
    {
        return r::min_element(m_path, {}, &Point::second)->second;
    }

    int max_y() const
    {
        return r::max_element(m_path, {}, &Point::second)->second;
    }

    friend std::ostream &operator<<(std::ostream &os, const Path &p)
    {
        for (const auto &[x, y] : p.m_path)
        {
            os << x << "," << y << " -> ";
        }
        return os;
    }

    void draw(cmatrix &grid)
    {
        std::span<Point> l1{m_path.begin(), m_path.size() - 1};
        std::span<Point> l2{m_path.begin() + 1, m_path.end()};
        for (const auto &[p1, p2] : v::zip(l1, l2))
        {
            if (p1.first == p2.first)
            {
                auto [s, e] = std::minmax(p1.second, p2.second);
                for (int i = s; i <= e; ++i)
                {
                    grid[i][p1.first] = '#';
                }
            }
            else
            {
                auto [s, e] = std::minmax(p1.first, p2.first);
                for (int i = s; i <= e; ++i)
                {
                    grid[p1.second][i] = '#';
                }
            }
        }
    }
};

bool move_sand_part1(cmatrix &grid, Point sand)
{
    while (true)
    {
        try
        {
            auto b = grid.at(sand.second + 1).at(sand.first);
            auto bl = grid.at(sand.second + 1).at(sand.first - 1);
            auto br = grid.at(sand.second + 1).at(sand.first + 1);
            if (b == '.')
            {
                sand.second++;
            }
            else if (bl == '.')
            {
                sand.first--;
                sand.second++;
            }
            else if (br == '.')
            {
                sand.first++;
                sand.second++;
            }
            else
            {
                grid[sand.second][sand.first] = 'o';
                return true;
            }
        }
        catch (std::out_of_range &)
        {
            return false;
        }
    }
}

bool move_sand_part2(Point sand, std::unordered_set<Point> &occupied_points, int max_depth)
{
    int depth = 0;
    while (depth < max_depth - 2)
    {
        auto b = Point{sand.first, sand.second + 1};
        auto bl = Point{sand.first - 1, sand.second + 1};
        auto br = Point{sand.first + 1, sand.second + 1};
        if (occupied_points.contains(b))
        {
            if (occupied_points.contains(bl))
            {
                if (occupied_points.contains(br))
                {
                    occupied_points.insert(sand);
                    return depth > 0 ? true : false;
                }
                else
                {
                    sand = br;
                }
            }
            else
            {
                sand = bl;
            }
        }
        else
        {
            sand = b;
        }
        ++depth;
    }
    occupied_points.insert(sand);
    return true;
}

int part1(cmatrix &grid, int min_x)
{
    int part1 = 0;
    while (move_sand_part1(grid, {500 - min_x, 0}))
    {
        ++part1;
    }
    return part1;
}

int part2(cmatrix &grid, int min_x)
{
    grid.push_back(std::vector<char>(grid.begin()->size(), '.'));
    grid.push_back(std::vector<char>(grid.begin()->size(), '#'));
    auto occupied_points = std::unordered_set<Point>{};
    for (int y = 0; y < grid.size(); ++y)
    {
        for (int x = 0; x < grid[y].size(); ++x)
        {
            if (grid[y][x] == '#')
            {
                occupied_points.insert({x, y});
            }
        }
    }
    int part2 = 0;
    while (move_sand_part2({500 - min_x, 0}, occupied_points, grid.size()))
    {
        ++part2;
    }
    return part2 + 1;
}

static void print_grid(const cmatrix &grid)
{
    for (const auto &row : grid)
    {
        for (const auto &c : row)
        {
            std::cout << c;
        }
        std::cout << '\n';
    }
}

int main()
{
    auto lines = read_file("data.txt");
    std::vector<Path> paths{};
    for (auto &line : lines)
    {
        paths.emplace_back(line);
    }
    int min_x = r::min_element(paths, {}, &Path::min_x)->min_x();
    int max_x = r::max_element(paths, {}, &Path::max_x)->max_x() - min_x;
    int min_y = r::min_element(paths, {}, &Path::min_y)->min_y();
    int max_y = r::max_element(paths, {}, &Path::max_y)->max_y();
    for (auto &path : paths)
    {
        path.normalize(min_x);
    }
    std::vector<std::vector<char>> grid(max_y + 1, std::vector<char>(max_x + 1, '.'));
    for (auto &path : paths)
    {
        path.draw(grid);
    }
    std::cout << part1(grid, min_x) << ' ';
    std::cout << part2(grid, min_x) << '\n';
}