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

enum class OpType { Mul, Do, Dont };

#if __cpp_lib_generator	== 202207L
std::generator<std::pair<size_t, OpType>> find_all(std::string_view str, std::string_view substr, OpType type) {
    size_t pos = str.find(substr, 0);
    while (pos != std::string::npos) {
        co_yield { pos, type };
        pos = str.find(substr, pos + 1);
    }
}
#else
std::vector<std::pair<size_t, OpType>> find_all(std::string_view str, std::string_view substr, OpType type) {
    std::vector<std::pair<size_t, OpType>> positions{};
    size_t pos = str.find(substr, 0);
    while (pos != std::string::npos) {
        positions.push_back({ pos, type });
        pos = str.find(substr, pos + 1);
    }
    return positions;
}
#endif

constexpr static std::string_view begin_mult{"mul("};
constexpr static std::string_view dop{"do()"};
constexpr static std::string_view dontp{"don't()"};

std::optional<std::pair<int64_t, int64_t>> verify_mul_op(std::string_view contents, size_t idx) {
    constexpr auto isnum = [](char c) { return c >= '0' && c <= '9'; };
    idx += begin_mult.size();
    // 1 to 3 numbers, comma, 1 to 3 numbers, closing parenthesis
    size_t count_num = 0;
    int64_t left = 0;
    int64_t right = 0;
    while (isnum(contents[idx]) && contents.size() > idx) {
        left = left * 10 + (contents[idx] - '0');
        ++count_num;
        ++idx;
    }
    if (count_num < 1 || count_num > 3) {
        return std::nullopt;
    }
    if (contents[idx] != ',' || contents.size() <= idx) {
        return std::nullopt;
    }
    ++idx;
    count_num = 0;
    while (isnum(contents[idx]) && contents.size() > idx) {
        right = right * 10 + (contents[idx] - '0');
        ++count_num;
        ++idx;
    }
    if (count_num < 1 || count_num > 3) {
        return std::nullopt;
    }
    if (contents[idx] != ')' || contents.size() <= idx) {
        return std::nullopt;
    }
    return std::make_pair(left, right);
}


int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    bool mult_enabled = true;
    auto idxs = v::join(std::array{ find_all(lines, begin_mult, OpType::Mul), find_all(lines, dop, OpType::Do), find_all(lines, dontp, OpType::Dont) }) | r::to<std::vector>();
    r::sort(idxs, [](const auto& lhs, const auto& rhs) {
        return lhs.first < rhs.first;
    });
    auto parts = r::fold_left(idxs, std::pair<int64_t, int64_t>{0, 0}, [&mult_enabled, &lines](auto&& accum, auto&& el) {
        int64_t p1 = accum.first;
        int64_t p2 = accum.second;
        switch (el.second) {
            case OpType::Mul:
                if (auto val = verify_mul_op(lines, el.first); val.has_value()) {
                    if (mult_enabled) {
                        p2 += val.value().first * val.value().second;
                    }
                    p1 += val.value().first * val.value().second;
                }
                break;
            case OpType::Do:
                mult_enabled = true;
                break;
            case OpType::Dont:
                mult_enabled = false;
                break;
        }
        return std::make_pair(p1, p2);
    });
    std::println("{} {}", parts.first, parts.second);
}