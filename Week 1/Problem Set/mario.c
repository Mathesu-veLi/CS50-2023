#include <cs50.h>
#include <stdbool.h>
#include <stdio.h>

int get_height(void);
void print_pyramid(int height_of_pyramid);
void print_a_collum(int row_length, int height_of_pyramid, bool is_left);
void print_the_spaces(int height_of_pyramid, int row_length);

int main(void)
{
    int height = get_height();

    print_pyramid(height);
}

int get_height(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    return height;
}

void print_pyramid(int height_of_pyramid)
{
    for (int row = 0; row < height_of_pyramid; row++)
    {

        print_a_collum(row, height_of_pyramid, true);

        printf("  ");

        print_a_collum(row, height_of_pyramid, false);

        printf("\n");
    }
}

void print_a_collum(int row_length, int height_of_pyramid, bool is_left)
{
    if (is_left)
    {
        print_the_spaces(height_of_pyramid, row_length);
    }

    for (int column = 0; column <= row_length; column++)
    {
        printf("#");
    }
}

void print_the_spaces(int height_of_pyramid, int row_length)
{
    for (int spaces = 0; spaces < height_of_pyramid - row_length - 1; spaces++)
    {
        printf(" ");
    }
}
