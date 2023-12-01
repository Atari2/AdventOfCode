#include <stdio.h>

#if 0
#define FILENAME "sample_data.txt"
#else
#define FILENAME "data.txt"
#endif


int main() {
    FILE *fp = fopen(FILENAME, "r");
    if (fp == NULL) {
        printf("Error opening file " FILENAME "\n");
        return 1;
    }
    int top_three[3] = {-1, -1, -1};

    char line[256];

    int value = 0;

    while (fgets(line, sizeof(line), fp)) {
        if (line[0] == '\n'){
            value = 0;
            continue;
        }
        value += atoi(line);
        for (int i = 0; i < 3; i++) {
            if (value > top_three[i]) {
                for (int j = 2; j >= i; j--) {
                    top_three[j] = top_three[j - 1];
                }
                top_three[i] = value;
                break;
            }
        }
    }
    int sum = 0;
    for (int i = 0; i < 3; i++) {
        sum += top_three[i];
    }

    printf("%d %d", top_three[0], sum);
    return 0;
}