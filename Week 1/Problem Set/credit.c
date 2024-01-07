#include <cs50.h>
#include <stdio.h>
#include <string.h>

int validate_credit_card(long long credit_card);
int get_number_of_digits(long long credit_card);
int get_the_doble_of_digit(int digit);
int get_the_digits_of_the_number(int number);
void indetify_credit_card(long long credit_card);
int get_the_two_first_digits_of_a_number(long long number);

int main(void)
{
    long long credit_card = get_long_long("Number: ");

    if (validate_credit_card(credit_card) == 0)
    {
        printf("INVALID\n");
    }
    else
    {
        indetify_credit_card(credit_card);
    }
}

int validate_credit_card(long long credit_card)
{
    int sum = 0;
    long long last_digit;
    int number_of_digits = get_number_of_digits(credit_card);

    for (int iterator = 0; iterator < number_of_digits; iterator++)
    {
        last_digit = credit_card;
        last_digit %= 10;

        if (iterator % 2 == 0)
        {
            sum += last_digit;
        }
        else
        {
            sum += get_the_doble_of_digit(last_digit);
        }

        credit_card /= 10;
    }

    if (sum % 10 > 0)
    {
        return 0;
    }
    return 1;
}

int get_number_of_digits(long long credit_card)
{
    int number_of_digits;
    for (number_of_digits = 0; credit_card; credit_card /= 10)
    {
        number_of_digits++;
    }

    return number_of_digits;
}

int get_the_doble_of_digit(int digit)
{
    int double_of_digit = digit * 2;

    if (double_of_digit > 9)
    {
        double_of_digit = get_the_digits_of_the_number(double_of_digit);
    }

    return double_of_digit;
}

int get_the_digits_of_the_number(int number)
{
    int number_of_digits = 0;
    int digit_of_number;

    while (number > 0)
    {
        digit_of_number = number;
        digit_of_number %= 10;

        number_of_digits += digit_of_number;

        number /= 10;
    }

    return number_of_digits;
}

void indetify_credit_card(long long credit_card)
{
    int number_of_digits = get_number_of_digits(credit_card);

    int twoFirstDigits = get_the_two_first_digits_of_a_number(credit_card);
    int firstDigit = twoFirstDigits / 10 % 10;

    bool mastercard_first_digits =
        twoFirstDigits == 51 || twoFirstDigits == 52 || twoFirstDigits == 53 || twoFirstDigits == 54 || twoFirstDigits == 55;

    if ((number_of_digits == 13 || number_of_digits == 16) && firstDigit == 4)
    {
        printf("VISA\n");
    }
    else if (number_of_digits == 15 && (twoFirstDigits == 34 || twoFirstDigits == 37))
    {
        printf("AMEX\n");
    }
    else if (number_of_digits == 16 && mastercard_first_digits)
    {
        printf("MASTERCARD\n");
    }
    else
    {
        printf("INVALID\n");
    }
}

int get_the_two_first_digits_of_a_number(long long number)
{
    while (number > 100)
    {
        number /= 10;
    }

    return number;
}
