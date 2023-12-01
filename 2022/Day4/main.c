#include <stdio.h>
#include <string.h>

#if 0
#define FILENAME "sample_data.txt"
#else
#define FILENAME "data.txt"
#endif

int main()
{
    FILE *fp = fopen(FILENAME, "r");
    if (fp == NULL)
    {
        printf("Error opening file " FILENAME "\n");
        return 1;
    }
    char buf[256];
    int count_part1 = 0;
    int count_part2 = 0;
    while (fgets(buf, sizeof(buf), fp))
    {
        int x1, y1, x2, y2;
        sscanf(buf, "%d-%d,%d-%d", &x1, &y1, &x2, &y2);
        if (((y1 <= y2) && (x1 >= x2)) || ((y1 >= y2) && (x1 <= x2)))
        {
            count_part1 += 1;
            count_part2 += 1;
        }
        else if (((x1 >= x2) && (x1 <= y2)) || ((x2 >= x1) && (x2 <= y1)))
        {
            count_part2 += 1;
        }
    }
    printf("%d %d", count_part1, count_part2);
    return 0;
}