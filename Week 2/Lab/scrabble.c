#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // TODO: Print the winner

    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
        return 0;
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
        return 0;
    }
    printf("Tie!\n");
}

int compute_score(string word)
{
    // TODO: Compute and return score for strin
    int word_length = strlen(word);
    int total_points = 0;

    for (int c = 0; c < word_length; c++)
    {
        int letter_int = toupper(word[c]) - '0';

        if (letter_int >= 17 && letter_int <= 42)
        {
            int points_of_letter = POINTS[letter_int - 17];
            total_points += points_of_letter;
        }
    };

    return total_points;
}
