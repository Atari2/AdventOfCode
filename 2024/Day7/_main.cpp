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

std::vector<std::string> read_file(std::string_view filename) {
    std::ifstream file(filename.data());
    std::vector<std::string> lines;
    std::string line;
    while (std::getline(file, line)) {
        lines.push_back(line);
    }
    return lines;
}

enum class Part { One, Two };
enum class Op { Add, Mul, Concat };

template <>
struct std::formatter<Op> : std::formatter<std::string_view> {

    template <typename ParseContext>
    constexpr auto parse(ParseContext& ctx) { return std::formatter<std::string_view>::parse(ctx); }

    template <typename FormatContext>
    auto format(Op op, FormatContext& ctx) const {
        std::string_view name;
        switch (op) {
            case Op::Add: name = "+"; break;
            case Op::Mul: name = "*"; break;
            case Op::Concat: name = "||"; break;
        }
        return std::formatter<std::string_view>::format(name, ctx);
    }
};

#if 0
std::generator<std::vector<Op>> product(r::range auto&& v, size_t repeat, std::vector<Op> current = {}) {
    if (current.size() == repeat) {
        co_yield current;
    } else {
        for (const auto& item : v) {
            current.push_back(item); 
            for (const auto& result : product(v, repeat, current)) {
                co_yield result;
            }
            current.pop_back();
        }
    }
}
#else
// FIXME: this shit doesn't work correctly.
template <r::range R>
class ProductIterator {
public:
    using ValueType = std::vector<Op>;

    ProductIterator(const R& elements, size_t repeat)
        : elements{elements}, repeat{repeat}, indices(repeat, 0), current{generate_current()}, done{repeat == 0} {
            advance();
        }

    ProductIterator& operator++() {
        advance();
        return *this;
    }

    const ValueType& operator*() const { return current.value(); }

    const ValueType* operator->() const { return &current.value(); }

    bool operator!=(std::default_sentinel_t) const { return !done; }

private:
    const R& elements;                    
    size_t repeat;                         
    std::vector<size_t> indices;           
    std::optional<ValueType> current;     
    bool done = false;                     

    std::optional<ValueType> generate_current() {
        if (done) return std::nullopt;
        ValueType result;
        result.reserve(indices.size());
        for (size_t i : indices) {
            result.push_back(elements[i]);
        }
        return result;
    }

    void advance() {
        for (size_t i = repeat; i-- > 0;) {
            if (++indices[i] < elements.size()) {
                current = generate_current();
                return;
            }
            indices[i] = 0;
        }
        done = true;
        current.reset();
    }
};

template <r::range R>
class ProductRange {
public:

    ProductRange(const R& elements, size_t repeat)
        : elements{elements}, repeat{repeat} {}

    auto begin() const { return ProductIterator{elements, repeat}; }
    std::default_sentinel_t end() const { return {}; }

private:
    const R& elements;
    size_t repeat;
};

auto product(r::range auto&& elements, size_t repeat) {
    return ProductRange{elements, repeat};
}
#endif

uint64_t concatenate(uint64_t a, uint64_t b) {
    static constexpr const uint64_t powersOfTen[] = {
        1, 10, 100, 1000, 10000, 100000, 1000000,
        10000000, 100000000, 1000000000, 10000000000,
        100000000000, 1000000000000, 10000000000000,
        100000000000000, 1000000000000000, 10000000000000000,
        100000000000000000, 1000000000000000000
    };
    uint64_t digits = 0;
    if (b == 0) { 
        digits = 1; 
    } else {
        unsigned long index; 
        #ifdef _MSC_VER
        _BitScanReverse64(&index, b); 
        #else
        index = 63 - __builtin_clzll(b);
        #endif
        digits = 1 + index * 30103 / 100000;
        if (b >= powersOfTen[digits]) { ++digits; }
    }
    return a * powersOfTen[digits] + b;
}

struct Equation {
    uint64_t expected_result;
    std::vector<uint64_t> operands;
    const static inline std::vector<Op> opsp1{Op::Add, Op::Mul};
    const static inline std::vector<Op> opsp2{Op::Add, Op::Mul, Op::Concat};

    Equation(const std::string& line) {
        auto v = line | v::split(':') | v::take(2);
        auto it = v.begin();
        std::from_chars((*it).data(), (*it).data() + (*it).size(), expected_result);
        it++;
        operands = *it | v::drop_while([](char c) { return c == ' '; }) | v::split(' ') | v::transform([](auto&& s) {
            uint64_t value = 0;
            std::from_chars(s.data(), s.data() + s.size(), value);
            return value;
        }) | r::to<std::vector>();
    }  

    uint64_t solve(Part part) {
        std::span possible_ops = part == Part::One ? opsp1 : opsp2;
        for (auto&& ops : product(possible_ops, operands.size() - 1)) {
            auto result = operands.front();
            for (auto&& [op, val] : v::zip(ops, operands | v::drop(1))) {
                switch (op) {
                    case Op::Add: result += val; break;
                    case Op::Mul: result *= val; break;
                    case Op::Concat: result = concatenate(result, val); break;
                }
            }
            if (result == expected_result) {
                return result;
            }
        }
        return 0;
    }
};

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    auto equations = lines | v::transform([](auto&& line) { return Equation(line); }) | r::to<std::vector>();
    auto part1 = r::fold_left(equations | v::transform([](auto&& eq) { return eq.solve(Part::One); }), 0, std::plus{});
    auto part2 = r::fold_left(equations | v::transform([](auto&& eq) { return eq.solve(Part::Two); }), 0, std::plus{});
    std::println("{} {}", part1, part2);
}
