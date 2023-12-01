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
    const int rps_mat[3][3] = {
        {3, 6, 0},
        {0, 3, 6},
        {6, 0, 3}
    };
    const int tr_mat[9][2] = {
        {3, 0}, {1, 3}, {2, 6},
        {1, 0}, {2, 3}, {3, 6},
        {2, 0}, {3, 3}, {1, 6}
    };
    char line[256];
    int tot_score_1 = 0;
    int tot_score_2 = 0;
    while (fgets(line, sizeof(line), fp)) {
        char a, b;
        sscanf(line, "%c %c", &a, &b);
        int x = a - 'A';
        int y = b - 'X';
        tot_score_1 += rps_mat[x][y] + y + 1;
        tot_score_2 += tr_mat[x * 3 + y][0] + tr_mat[x * 3 + y][1];
    }
    printf("%d %d", tot_score_1, tot_score_2);
    return 0;
}