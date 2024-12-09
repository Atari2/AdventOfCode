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
using namespace std::string_literals;

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

int64_t part1(std::vector<int64_t> filesystem) {
    size_t i = filesystem.size() - 1;
    size_t latest_idx = 0;
    for (const auto& c : filesystem | v::reverse) {
        if (auto it = r::find(filesystem.begin() + latest_idx, filesystem.end(), -1); it != filesystem.end()) {
            latest_idx = std::distance(filesystem.begin(), it);
            filesystem[latest_idx] = c;
            filesystem[i] = -2;
            i -= 1;
        } else {
            break;
        }
    }
    int64_t tot = 0;
    for (auto&& [i, c] : filesystem | v::enumerate) {
        if (c >= 0) {
            tot += (i * c);
        } else {
            break;
        }
    }
    return tot;
} 

int64_t part2(std::vector<int64_t> filesystem) {
    int64_t curtype = filesystem[0];
    auto spaces = curtype == -1 ? std::vector<std::pair<int64_t, int64_t>>{{0, 0}} : std::vector<std::pair<int64_t, int64_t>>{};
    auto files = curtype != -1 ? std::vector<std::pair<int64_t, int64_t>>{{0, 0}} : std::vector<std::pair<int64_t, int64_t>>{};
    for (auto&& [i, c] : filesystem | v::enumerate) {
        if (curtype == -1) {
            if (c == -1) {
                spaces.back().second += 1;
            } else {
                curtype = c;
                files.push_back({i, 1});
            }
        } else {
            if (c == -1) {
                curtype = -1;
                spaces.push_back({i, 1});
            } else if (c == curtype) {
                files.back().second += 1;
            } else {
                curtype = c;
                files.push_back({i, 1});
            }
        }
    }
    for (auto&& [n, f] : v::zip(v::iota(size_t{0}, files.size()) | v::reverse, files | v::reverse)) {
        auto&& [file_idx, file_size] = f;
        for (auto&& [i, s] : spaces | v::enumerate) {
            auto&& [space_idx, space_size] = s;
            if (space_idx > file_idx) break;
            if (file_size <= space_size) {
                r::fill_n(filesystem.begin() + space_idx, file_size, n);
                r::fill_n(filesystem.begin() + file_idx, file_size, -1);
                spaces[i] = {space_idx + file_size, space_size - file_size};
                break;
            }
        }
    }
    int64_t tot = 0;
    for (auto&& [i, c] : filesystem | v::enumerate) {
        if (c != -1) {
            tot += (i * c);
        }
    }
    return tot;
}

int main() {
    auto data = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    std::vector<int64_t> fs{};
    fs.reserve(data.size());
    for (auto&& [i, f] : data | v::chunk(2) | v::enumerate) {
        auto fit = f.begin();
        r::fill_n(std::back_inserter(fs), (size_t)(*fit - '0'), i);
        if (++fit != f.end()) {
            r::fill_n(std::back_inserter(fs), (size_t)(*fit - '0'), -1);
        }
    }
    std::println("{} {}", part1(fs), part2(fs));
}
