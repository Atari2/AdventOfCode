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

struct Wire {
    std::string name;
    std::optional<bool> value;

    Wire(std::string_view name, std::optional<bool> value = std::nullopt) : name{name}, value{value} {}
    bool operator==(const Wire& other) const {
        return name == other.name;
    }
    bool operator==(std::string_view other_name) const {
        return name == other_name;
    }
    bool has_value() const {
        return value.has_value();
    }
};

enum class GateType {
    AND,
    OR,
    XOR
};

struct Gate {
    GateType type;
    std::pair<Wire*, Wire*> inputs;
    Wire* output;

    public:
    Gate(GateType type, Wire* input1, Wire* input2, Wire* output) : type{type}, inputs{input1, input2}, output{output} {}
    static Gate from_string(std::string_view input, std::vector<std::unique_ptr<Wire>>& existing_wires) {
        auto parts = input | v::split(' ') | v::transform([](auto&& str) {
            return std::string_view{str};
        }) | r::to<std::vector>();
        auto find_wire = [&](std::string_view name) -> Wire* {
            auto it = r::find_if(existing_wires, [&](const auto& w) {
                return *w == name;
            });
            if (it != existing_wires.end()) {
                return it->get();
            } else {
                auto new_wire = std::make_unique<Wire>(name);
                existing_wires.push_back(std::move(new_wire));
                return existing_wires.back().get();
            }
        };
        GateType type;
        if (parts[1] == "AND"sv) {
            type = GateType::AND;
        } else if (parts[1] == "OR"sv) {
            type = GateType::OR;
        } else if (parts[1] == "XOR"sv) {
            type = GateType::XOR;
        } else {
            throw std::runtime_error("Unknown gate type");
        }
        auto input1 = find_wire(parts[0]);
        auto input2 = find_wire(parts[2]);
        auto output = find_wire(parts[4]);
        return Gate{type, input1, input2, output};
    };
    bool can_be_calculated() const {
        return inputs.first->has_value() && inputs.second->has_value();
    }
    bool calculated() const {
        return output->has_value();
    }
    void calculate() {
        switch (type) {
            case GateType::AND:
                output->value = inputs.first->value.value() & inputs.second->value.value();
                break;
            case GateType::OR:
                output->value = inputs.first->value.value() | inputs.second->value.value();
                break;
            case GateType::XOR:
                output->value = inputs.first->value.value() ^ inputs.second->value.value();
                break;
        }
    }
};

template <>
struct std::hash<Wire> {
    constexpr static inline std::hash<std::string> hasher{};
    std::size_t operator()(const Wire& w) const noexcept {
        return hasher(w.name);
    }
};

char is_xyz(std::string_view v) {
    char c = v.front();
    return c == 'x' || c == 'y' || c == 'z';
}

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt"sv : "data.txt"sv);
    std::vector<std::unique_ptr<Wire>> wires;
    std::vector<Gate> gates;
    bool parsing_wires = true;
    for (const auto& line : lines) {
        if (line.empty()) {
            parsing_wires = false;
            continue;
        }
        if (parsing_wires) {
            auto parts = line | v::split(':') | v::transform([](auto&& str) {
                return std::string_view{str};
            }) | r::to<std::vector>();
            if (parts.size() == 2) {
                wires.emplace_back(std::make_unique<Wire>(parts[0], parts[1].back() == '1'));
            } else {
                wires.emplace_back(std::make_unique<Wire>(parts[0]));
            }
        } else {
            gates.push_back(Gate::from_string(line, wires));
        }
    }
    
    auto z_wires = wires | v::transform([](const auto& w) { return w.get(); }) | v::filter([](const auto& w) {
        return w->name.front() == 'z';
    }) | r::to<std::vector>();
    r::sort(z_wires, [](const auto& a, const auto& b) {
        return a->name > b->name;
    });
    while (!r::all_of(z_wires, [](const auto& w) {
               return w->has_value();
           })) {
        for (auto& gate : gates) {
            if (gate.can_be_calculated() && !gate.calculated()) {
                gate.calculate();
            }
        }
    }
    auto part1bin = z_wires | v::transform([](const auto& w) {
        return w->value.value() ? '1' : '0';
    }) | r::to<std::string>();
    size_t part1 = 0;
    std::from_chars(part1bin.data(), part1bin.data() + part1bin.size(), part1, 2);
    Wire* highest_z = z_wires.front();
    std::unordered_set<Wire> wrong{};
    for (auto& gate : gates) {
        if (gate.output->name.front() == 'z' && gate.type != GateType::XOR && gate.output != highest_z) {
            wrong.insert(*gate.output);
        }
        if (gate.type == GateType::XOR
            && !is_xyz(gate.inputs.first->name)
            && !is_xyz(gate.inputs.second->name)
            && !is_xyz(gate.output->name)) {
            wrong.insert(*gate.output);
        }
        if (gate.type == GateType::AND && (gate.inputs.first->name != "x00" && gate.inputs.second->name != "x00")) {
            for (auto& subgate : gates) {
                if ((gate.output == subgate.inputs.first || gate.output == subgate.inputs.second) && subgate.type != GateType::OR) {
                    wrong.insert(*gate.output);
                }
            }
        }
        if (gate.type == GateType::XOR) {
            for (auto& subgate : gates) {
                if ((gate.output == subgate.inputs.first || gate.output == subgate.inputs.second) && subgate.type == GateType::OR) {
                    wrong.insert(*gate.output);
                }
            }
        }
    }
    auto wrong_names = wrong | v::transform([](const auto& w) {
        return w.name;
    }) | r::to<std::vector>();
    r::sort(wrong_names);
    auto part2 = wrong_names | v::join_with(',') | r::to<std::string>();
    std::print("{} {}\n", part1, part2);
    return 0;
}