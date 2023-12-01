#include <fstream>
#include <iostream>
#include <string>
#include <string_view>
#include <vector>
#include <unordered_map>
#include <optional>
#include <ranges>
#include <memory>
#include <concepts>
#include <algorithm>
#include <numeric>
#include <array>

constexpr int MINUTES = 30;

std::vector<std::string> read_file(std::string_view filename) {
    std::ifstream file(filename.data());
    std::vector<std::string> lines;
    std::string line;
    while (std::getline(file, line)) {
        lines.push_back(line);
    }
    return lines;
}

enum class State : bool {
    OPEN,
    CLOSED
};

namespace v = std::ranges::views;
namespace r = std::ranges;
using namespace std::string_view_literals;
struct Valve;


template <typename T>
concept string_like = std::same_as<T, std::string> || std::same_as<T, std::string_view>;

struct HashTo {
    using is_transparent = void;
    std::size_t operator()(const string_like auto& o) const {
        using T = std::remove_cvref_t<decltype(o)>;
        return std::hash<T>{}(o);
    }
};

struct EqualTo {
    using is_transparent = void;
    constexpr bool operator()(const string_like auto& lhs,  const string_like auto& rhs) const {
        return std::string_view{lhs} == std::string_view{rhs};
    }
};


using ValveMap = std::unordered_map<std::string, std::shared_ptr<Valve>, HashTo, EqualTo>;

struct Valve {
    std::string name;
    std::optional<int> _flow_rate;
    std::array<int, MINUTES> flow_rate_minutes{};
    ValveMap tunnels;
    State state;

    template <typename T>
    using opt = std::optional<T>;
    static constexpr auto to_str = [](auto &&subr) { return std::string{subr.begin(), subr.end()}; };

    constexpr static auto none = std::nullopt;

    Valve(const Valve& other) : name(other.name), _flow_rate(other._flow_rate), flow_rate_minutes(other.flow_rate_minutes), tunnels(other.tunnels), state(other.state) {

    }

    Valve(Valve&& other) : name(std::move(other.name)), _flow_rate(std::move(other._flow_rate)), flow_rate_minutes(other.flow_rate_minutes), tunnels(std::move(other.tunnels)), state(other.state) {

    }

    Valve(std::string_view _name, opt<int> flow_rate = none, opt<std::string_view> tunnelstr = none, ValveMap* valves = nullptr) 
    : name(_name), _flow_rate(std::move(flow_rate)), tunnels{}
    {
        this->state = State::CLOSED;
        if (tunnelstr.has_value() && valves != nullptr) {
            set_tunnels(tunnelstr.value(), *valves);
        }
    }

    int flow_rate() const {
        if (this->_flow_rate.has_value()) {
            return this->_flow_rate.value();
        }
        return 0;
    }

    int flow_rate(int i) const {
        if (this->_flow_rate.has_value()) {
            return this->flow_rate_minutes[i];
        }
        return 0;
    }

    void set_flow_rate(int flow_rate) {
        this->_flow_rate = flow_rate;
        if (flow_rate > 0) {
            for (int i = 0; i < MINUTES; i++) {
                this->flow_rate_minutes[i] = flow_rate * (MINUTES - i);
            }
        }
    }

    void set_tunnels(std::string_view tunnelstr, ValveMap& valves) {
        for (const auto& tunnel : v::split(tunnelstr, ", "sv) | v::transform(to_str)) {
            auto it = valves.find(tunnel);
            if (it == valves.end()) {
                it = valves.insert({tunnel, std::make_shared<Valve>(tunnel)}).first;
            }
            this->tunnels.insert(*it);
        }
    }
};


int main() {
    auto lines = read_file("sample_data.txt");
    ValveMap valves;
    for (const auto& line : lines) {
        char name[256];
        int flow_rate = 0;
        int ptr;
        sscanf(line.data(), "Valve %s has flow rate=%d; tunnels lead to valves %n", name, &flow_rate, &ptr);
        std::string sname{name};
        std::string_view tunnelstr{line.data() + ptr};
        if (auto it = valves.find(sname); it != valves.end()) {
            it->second->set_flow_rate(flow_rate);
            it->second->set_tunnels(tunnelstr, valves);
        } else {
            valves.insert({sname, std::make_shared<Valve>(sname, flow_rate, tunnelstr, &valves)});
        }
    }
    auto current_valve = valves["AA"];
    int tot_pressure = 0;
    for (int i = 0; i < MINUTES; ++i) {
        if (current_valve->flow_rate() > 0 && current_valve->state == State::CLOSED) {
            current_valve->state = State::OPEN;
            tot_pressure += current_valve->flow_rate(i);
            std::cout << "Valve " << current_valve->name << " is open at minute " << (i+1) << '\n';
        } else {
            auto filter = v::transform(current_valve->tunnels, [](const auto& v){ return v.second; }) | v::filter([](const auto& v) { return v->state == State::CLOSED; });
            current_valve = r::max(filter, {}, [i](const auto& v) { return v->flow_rate(i); });
            std::cout << "Moving to " << current_valve->name << " at minute " << (i+1) << '\n';
        }
    }
    std::cout << "Total pressure: " << tot_pressure << '\n';
    return 0;
}