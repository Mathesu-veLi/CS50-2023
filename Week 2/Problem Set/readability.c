#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int get_total_letters(string text);
int get_total_words(string text);
int get_total_sentences(string text);
float get_grade(float letters, float words, float sentences);

int main(void)
{
    string text = get_string("Text: ");

    float letters = get_total_letters(text);
    float words = get_total_words(text);
    float sentences = get_total_sentences(text);

    float grade = get_grade(letters, words, sentences);

    if (grade >= 16)
    {
        printf("Grade 16+\n");
        return 0;
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
        return 0;
    }

    printf("Grade %.0f\n", grade);
}

int get_total_letters(string text)
{
    int letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            letters += 1;
        }
    }

    return letters;
}

int get_total_words(string text)
{
    int words = 1;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isspace(text[i]))
        {
            words += 1;
        }
    }

    return words;
}

int get_total_sentences(string text)
{
    int sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if ((text[i] == '!') || (text[i] == '?') || (text[i] == '.'))
        {
            sentences += 1;
        }
    }

    return sentences;
}

float get_grade(float letters, float words, float sentences)
{
    float L = (letters / words) * 100;
    float S = (sentences / words) * 100;
    float grade = (0.0588 * L) - (0.296 * S) - 15.8;

    return grade;
}
