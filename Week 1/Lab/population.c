#include <cs50.h>
#include <stdio.h>

int get_initial_number_of_llamas(void);
int get_final_number_of_llamas(int initial_number_of_llamas);
int get_years_to_the_final_number_of_llamas(int initial_number_of_llamas, int final_number_of_llamas);

int main(void)
{

    int start = get_initial_number_of_llamas();

    int end = get_final_number_of_llamas(start);

    int years = get_years_to_the_final_number_of_llamas(start, end);

    printf("Years: %i\n", years);
}

int get_initial_number_of_llamas(void)
{
    int start;
    do
    {
        start = get_int("Start size: ");
    }
    while (start < 9 || start < 1);

    return start;
}

int get_final_number_of_llamas(int initial_number_of_llamas)
{
    int end;
    do
    {
        end = get_int("End size: ");
    }
    while (end < initial_number_of_llamas || end < 1);

    return end;
}

int get_years_to_the_final_number_of_llamas(int initial_number_of_llamas, int final_number_of_llamas)
{
    int years = 0;
    while (initial_number_of_llamas < final_number_of_llamas)
    {
        initial_number_of_llamas = initial_number_of_llamas + (initial_number_of_llamas / 3) - (initial_number_of_llamas / 4);
        years++;
    }

    return years;
}
