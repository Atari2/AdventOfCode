#include <stdio.h>
#include <string.h>

#if 0
#define FILENAME "sample_data.txt"
#else
#define FILENAME "data.txt"
#endif

int part1() {
    FILE *fp = fopen(FILENAME, "r");
    if (fp == NULL) {
        printf("Error opening file " FILENAME "\n");
        return -1;
    }
    const char values[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const size_t values_len = sizeof(values);
    char buf[256];
    char half1[256];
    char half2[256];
    int tot = 0;
    while (fgets(buf, sizeof(buf), fp)) {
        size_t len = strlen(buf);
        memcpy(half1, buf, len / 2);
        half1[len / 2] = '\0';
        memcpy(half2, buf + len / 2, len / 2);
        half2[len / 2] = '\0';
        for (int i = 0; i < values_len; i++) {
            char* ptr1 = strchr(half1, values[i]);
            char* ptr2 = strchr(half2, values[i]);
            if (ptr1 && ptr2) {
                tot += i + 1;
                break;
            }
        }
    }
    return tot;
}

int part2() {
    FILE *fp = fopen(FILENAME, "r");
    if (fp == NULL) {
        printf("Error opening file " FILENAME "\n");
        return -1;
    }
    const char values[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const size_t values_len = sizeof(values);
    char buf1[256];
    char buf2[256];
    char buf3[256];
    char* bufs[3] = { buf1, buf2, buf3 };
    int counter = 0;
    int tot = 0;
    while (fgets(bufs[counter], sizeof(buf1), fp)) {
        if (++counter == 3) {
            counter = 0;
            for (int i = 0; i < values_len; i++) {
                char* ptr1 = strchr(bufs[0], values[i]);
                char* ptr2 = strchr(bufs[1], values[i]);
                char* ptr3 = strchr(bufs[2], values[i]);
                if (ptr1 && ptr2 && ptr3) {
                    tot += i + 1;
                    break;
                }
            }
        }
    }
    return tot;
}

int main() {
    printf("%d %d", part1(), part2());
    return 0;
}