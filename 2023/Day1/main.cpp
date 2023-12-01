#include <version>
#include <fstream>
#include <string>
#include <string_view>
#include <vector>
#include <array>

constexpr bool SAMPLE_DATA = false;

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


int main() {
    auto lines = read_file(SAMPLE_DATA ? "sample_data.txt" : "data.txt");
    size_t totalp1 = 0;
    size_t totalp2 = 0;
    constexpr std::array digitwords = {
        "one"sv, "two"sv, "three"sv, "four"sv,
        "five"sv, "six"sv, "seven"sv, "eight"sv, "nine"sv
    };
    for (const auto& line : lines) {
        auto first_digit_idx = line.find_first_of("0123456789"sv);
        auto last_digit_idx = line.find_last_of("0123456789"sv);
        size_t first_digit = line[first_digit_idx] - '0';
        size_t last_digit = line[last_digit_idx] - '0';
        totalp1 += first_digit * 10 + last_digit;
        for (size_t i = 0; i < digitwords.size(); ++i) {
            const auto& digword = digitwords[i];
            if (auto idx = line.find(digword); idx != std::string::npos) {
                if (idx < first_digit_idx) {
                    first_digit_idx = idx;
                    first_digit = i + 1;
                }
                if (idx > last_digit_idx) {
                    last_digit_idx = idx;
                    last_digit = i + 1;
                }
            }
            if (auto idx = line.rfind(digword); idx != std::string::npos) {
                if (idx < first_digit_idx) {
                    first_digit_idx = idx;
                    first_digit = i + 1;
                }
                if (idx > last_digit_idx) {
                    last_digit_idx = idx;
                    last_digit = i + 1;
                }
            }
        }
        totalp2 += first_digit * 10 + last_digit;
    }
    printf("%zu %zu\n", totalp1, totalp2);
    return 0;
}