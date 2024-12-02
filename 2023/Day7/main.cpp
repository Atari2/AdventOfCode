// compile with: cl /nologo /O2 /EHsc /std:c++latest main.cpp
// most of this is just me playing around with C++23 ranges and views
#include <version>
#if __cpp_lib_ranges < 202207L
#error "This code requires C++23 range features"
#endif

#include <algorithm>
#include <charconv>
#include <fstream>
#include <ranges>
#include <string>
#include <string_view>
#include <vector>
#include <cstdio>
#include <unordered_map>
#include <span>
#include <iostream>

constexpr bool SAMPLE_DATA = false;

namespace r = std::ranges;
namespace v = std::ranges::views;
using namespace std::string_view_literals;

static constexpr std::array strengthsp1{
    'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'
};
static constexpr std::array strengthsp2{
    'A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J'
};

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
    auto first = line.find_first_not_of(" \t\n\v\f\r"sv);
    auto last = line.find_last_not_of(" \t\n\v\f\r"sv);
    return line.substr(first, last - first + 1);
}

std::pair<std::string_view, std::string_view> split_once(std::string_view orig, char delim, bool trim = true) {
    auto delim_pos = orig.find(delim);
    if (delim_pos == std::string_view::npos) {
        return {trim ? strip_view(orig) : orig, {}};
    }
    auto first = orig.substr(0, delim_pos);
    auto second = orig.substr(delim_pos + 1);
    if (trim) {
        first = strip_view(first);
        second = strip_view(second);
    }
    return {first, second};
}

enum class HandType : uint8_t {
    FiveOfAKind,
    FourOfAKind,
    FullHouse,
    ThreeOfAKind,
    TwoPair,
    OnePair,
    HighCard
};

struct Hand {
    char hand[5];
    int64_t bet{0};
    HandType hand_type{};
    Hand(std::string_view line) {
        auto [h, betstr] = split_once(line, ' ');
        std::memcpy(hand, h.data(), sizeof(hand));
        std::from_chars(betstr.data(), betstr.data() + betstr.size(), bet);
    }
};

struct HandPart1 : Hand {
    HandPart1(std::string_view line) : Hand(line) {
        std::unordered_map<char, int64_t> unique_cards{};
        for (auto c : hand) {
            unique_cards[c] += 1;
        }
        switch (unique_cards.size()) {
            case 1:
                hand_type = HandType::FiveOfAKind;
                break;
            case 2:
                if (r::any_of(unique_cards | v::values, [](auto&& v) { return v == 4; })) {
                    hand_type = HandType::FourOfAKind;
                } else {
                    hand_type = HandType::FullHouse;
                }
                break;
            case 3:
                if (r::any_of(unique_cards | v::values, [](auto&& v) { return v == 3; })) {
                    hand_type = HandType::ThreeOfAKind;
                } else {
                    hand_type = HandType::TwoPair;
                }
                break;
            case 4:
                hand_type = HandType::OnePair;
                break;
            case 5:
                hand_type = HandType::HighCard;
                break;
        }
    }

    bool operator<(const HandPart1& other) const {
        if (hand_type > other.hand_type) {
            return true;
        } else if (hand_type < other.hand_type) {
            return false;
        } else {
            for (const auto [sc, oc] : v::zip(hand, other.hand)) {
                auto idx = r::find(strengthsp1, sc);
                auto oidx = r::find(strengthsp1, oc);
                if (idx > oidx) {
                    return true;
                } else if (idx < oidx) {
                    return false;
                }
            }
        }
        return false;
    }
};

static void comb_rip(size_t pos, const std::span<const char>& items, std::string& sol, size_t k, size_t start, auto callback) {
    if (pos >= k) {
        callback(sol);
        return;
    }
    for (size_t i = start; i < items.size(); ++i) {
        sol[pos] = items[i];
        comb_rip(pos + 1, items, sol, k, i, std::forward<decltype(callback)>(callback));
        start++;
    }
}

static void combination_with_repetition(std::span<const char> items, size_t n, auto callback) {
    std::string sol(n, '\0');
    comb_rip(0, items, sol, n, 0, std::forward<decltype(callback)>(callback));
}

struct HandPart2 : Hand {
    private:

    HandType get_hand_type(char (&curhand)[5]) {
        std::unordered_map<char, int64_t> unique_cards{};
        for (auto c : curhand) {
            unique_cards[c] += 1;
        }
        switch (unique_cards.size()) {
            case 1:
                return HandType::FiveOfAKind;
            case 2:
                if (r::any_of(unique_cards | v::values, [](auto&& v) { return v == 4; })) {
                    return HandType::FourOfAKind;
                } else {
                    return HandType::FullHouse;
                }
            case 3:
                if (r::any_of(unique_cards | v::values, [](auto&& v) { return v == 3; })) {
                    return HandType::ThreeOfAKind;
                } else {
                    return HandType::TwoPair;
                }
            case 4:
                return HandType::OnePair;
            case 5:
                return HandType::HighCard;
        }
        return HandType::HighCard;
    }
    public:
    HandPart2(std::string_view line) : Hand(line) {
        auto j_count = r::count(hand, 'J');
        char curhand[5]{};
        std::memcpy(curhand, hand, sizeof(hand));
        if (j_count == 0) {
            hand_type = get_hand_type(curhand);
        } else {
            hand_type = HandType::HighCard;
            combination_with_repetition(std::span{strengthsp2.data(), strengthsp2.size() - 1}, static_cast<size_t>(j_count), [this, &curhand](const auto& comb){
                for (size_t i = 0, j = 0; i < sizeof(hand); ++i) {
                    if (hand[i] == 'J') {
                        curhand[i] = comb[j++];
                    } else {
                        curhand[i] = hand[i];
                    }
                }
                auto ht = get_hand_type(curhand);
                if (ht < hand_type) {
                    hand_type = ht;
                }
            });
        }
        
    }

    bool operator<(const HandPart2& other) const {
        if (hand_type > other.hand_type) {
            return true;
        } else if (hand_type < other.hand_type) {
            return false;
        } else {
            for (const auto [sc, oc] : v::zip(hand, other.hand)) {
                auto idx = r::find(strengthsp2, sc);
                auto oidx = r::find(strengthsp2, oc);
                if (idx > oidx) {
                    return true;
                } else if (idx < oidx) {
                    return false;
                }
            }
        }
        return false;
    }
};

int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt" : "data.txt");
    auto handsp1 = lines | v::transform([](auto&& line) { return HandPart1(line); }) | r::to<std::vector>();
    r::sort(handsp1, std::less<>{});
    auto totalp1 = r::fold_left(v::zip(handsp1, v::iota(1) | v::take(handsp1.size())), 0, [](auto&& acc, auto&& ih) { return acc + (std::get<0>(ih).bet * std::get<1>(ih)); });
    
    auto handsp2 = lines | v::transform([](auto&& line) { return HandPart2(line); }) | r::to<std::vector>();
    r::sort(handsp2, std::less<>{});
    auto totalp2 = r::fold_left(v::zip(handsp2, v::iota(1) | v::take(handsp2.size())), 0, [](auto&& acc, auto&& ih) { return acc + (std::get<0>(ih).bet * std::get<1>(ih)); });
    
    std::printf("%lld %lld\n", totalp1, totalp2);
}