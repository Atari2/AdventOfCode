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
#include <utility>

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

struct Cpu {
    std::vector<int64_t> program;
    int64_t pc;
    int64_t a;
    int64_t b;
    int64_t c;
    std::vector<std::string> output;

    Cpu(const std::vector<std::string>& data) {
        pc = 0;
        std::sscanf(data[0].data(), "Register A: %" SCNd64, &a);
        std::sscanf(data[1].data(), "Register B: %" SCNd64, &b);
        std::sscanf(data[2].data(), "Register C: %" SCNd64, &c);
        program = (*++(data[4] | v::split(':')).begin()) | v::drop(1) | v::split(',') | v::transform([](auto&& str) {
            int64_t value;
            std::from_chars(str.data(), str.data() + str.size(), value);
            return value;
        }) | r::to<std::vector>();
        output = {};
    }

    int64_t combo() {
        auto op = program[pc];
        switch (op) {
            case 0:
            case 1:
            case 2:
            case 3:
                return op;
            case 4:
                return a;
            case 5:
                return b;
            case 6:
                return c;
            default:
                throw std::runtime_error("Invalid opcode");
        }
    }

    void adv() {
        auto operand = combo();
        pc += 1;
        a = a / (1 << operand);
    }

    void bxl() {
        b = b ^ program[pc++];
    }

    void bst() {
        auto operand = combo();
        pc += 1;
        b = operand % 8;
    }

    void jnz() {
        if (a != 0) {
            pc = program[pc];
        } else {
            pc += 1;
        }
    }

    void bxc() {
        b = b ^ c;
        pc += 1;
    }

    void out() {
        auto operand = combo() % 8;
        pc += 1;
        output.push_back(std::to_string(operand));
    }

    int64_t outp2() {
        auto operand = combo() % 8;
        pc += 1;
        output.push_back(std::to_string(operand));
        return operand;
    }

    void bdv() {
        auto operand = combo();
        pc += 1;
        b = a / (1 << operand);
    }

    void cdv() {
        auto operand = combo();
        pc += 1;
        c = a / (1 << operand);
    }

    void run() {
        std::array instructions {
            &Cpu::adv, &Cpu::bxl, &Cpu::bst, &Cpu::jnz, &Cpu::bxc, &Cpu::out, &Cpu::bdv, &Cpu::cdv
        };
        while (pc < program.size()) {
            auto opcode = program[pc];
            pc += 1;
            (this->*instructions[opcode])();
        }
    }

    int64_t runp2() {
        while (pc < program.size()) {
            auto opcode = program[pc];
            pc += 1;
            switch (opcode) {
                case 0:
                    adv();
                    break;
                case 1:
                    bxl();
                    break;
                case 2:
                    bst();
                    break;
                case 3:
                    jnz();
                    break;
                case 4:
                    bxc();
                    break;
                case 5:
                    return outp2();
                case 6:
                    bdv();
                    break;
                case 7:
                    cdv();
                    break;
            }
        }
        return -1;
    }

    void reset() {
        pc = 0;
        a = 0;
        b = 0;
        c = 0;
        output.clear();
    }

    std::string result() const {
        return output | v::join_with(',') | r::to<std::string>(); 
    }

};

int64_t part2(const std::vector<std::string>& data) {
    auto cpu = Cpu(data);
    int64_t place = cpu.program.size() - 1;
    std::vector<int64_t> current_reg_as{0};

    while (place >= 0) {
        std::vector<int64_t> next_reg_as{};
        auto expected_output = cpu.program[place];
        for (auto a : current_reg_as) {
            auto newa = a * 8;
            for (int64_t i = 0; i < 8; ++i) {
                cpu.a = newa + i;
                auto output = cpu.runp2();
                cpu.reset();
                if (output == expected_output) {
                    next_reg_as.push_back(newa + i);
                }
            }
        }
        place -= 1;
        current_reg_as = next_reg_as;
    }

    return *std::min_element(current_reg_as.begin(), current_reg_as.end());
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    auto cpu = Cpu(lines);
    cpu.run();
    auto part1 = cpu.result();
    auto p2 = part2(lines);
    std::println("{} {}", part1, p2);
}