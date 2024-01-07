def get_grade(letters: int, words: int, sentences: int):
    L = (letters / words) * 100
    S = (sentences / words) * 100
    grade = (0.0588 * L) - (0.296 * S) - 15.8

    return grade


def get_total_sentences(text: str):
    sentences = 0
    for c in text:
        for i in ["!", "?", "."]:
            if i == c:
                sentences += 1

    return sentences


def get_total_words(text: str):
    words = 1
    for c in text:
        if c.isspace():
            words += 1

    return words


def get_total_letters(text: str):
    letters = 0
    for c in text:
        if c.isalpha():
            letters += 1

    return letters


def main():
    text = str(input("Text: "))

    letters = get_total_letters(text)
    words = get_total_words(text)
    sentences = get_total_sentences(text)

    grade = get_grade(letters, words, sentences)

    if grade >= 16:
        print("Grade 16+")
    elif grade < 1:
        print("Before Grade 1")

    print(f"Grade {round(grade)}")


if __name__ == "__main__":
    main()
