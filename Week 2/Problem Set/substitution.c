#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

string get_encrypted_message(string plaintext, string key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    if (strlen(argv[1]) < 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    for (int iterator = 0; iterator < strlen(argv[1]); iterator++)
    {
        if (!isalpha(argv[1][iterator]))
        {
            printf("Usage: ./substitution key\n");
            return 1;
        }
    }

    for (int iterator = 0; iterator < strlen(argv[1]); iterator++)
    {
        for (int second_iterator = iterator + 1; second_iterator < strlen(argv[1]); second_iterator++)
        {
            if (tolower(argv[1][second_iterator]) == tolower(argv[1][iterator]))
            {
                printf("Usage: ./substitution key\n");
                return 1;
            }
        }
    }

    string plaintext = get_string("plaintext: ");

    printf("ciphertext: %s\n", get_encrypted_message(plaintext, argv[1]));
    return 0;
}

string get_encrypted_message(string plaintext, string key)
{
    for (int iterator = 0; iterator < strlen(plaintext); iterator++)
    {
        int letter_value = plaintext[iterator];

        if (isalpha(plaintext[iterator]))
        {
            if (islower(plaintext[iterator]))
            {
                plaintext[iterator] = tolower(key[letter_value - 97]);
            }

            else
            {
                plaintext[iterator] = toupper(key[letter_value - 65]);
            }
        }
    }

    return plaintext;
}
