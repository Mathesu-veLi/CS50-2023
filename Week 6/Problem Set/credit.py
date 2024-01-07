def indetify_credit_card(credit_card_number: int):
    digits_quantity = len(str(credit_card_number))

    two_first_digits = int(str(credit_card_number)[0:2])
    first_digit = int(str(credit_card_number)[0])

    mastercard_first_digits = (
        two_first_digits == 51
        or two_first_digits == 52
        or two_first_digits == 53
        or two_first_digits == 54
        or two_first_digits == 55
    )

    if (digits_quantity == 13 or digits_quantity == 16) and first_digit == 4:
        print("VISA")
    elif digits_quantity == 15 and (two_first_digits == 34 or two_first_digits == 37):
        print("AMEX")
    elif digits_quantity == 16 and mastercard_first_digits:
        print("MASTERCARD")
    else:
        print("INVALID")


def double_digit(number: int):
    doubled_number = number * 2

    if doubled_number > 9:
        doubled_number = int(str(doubled_number)[0]) + int(str(doubled_number)[1])

    return doubled_number


def validate_credit_card(credit_card_number: int):
    sum = 0
    digits_quantity = len(str(credit_card_number))

    for iterator in range(digits_quantity):
        last_digit = int(str(credit_card_number)[digits_quantity - iterator - 1])

        if iterator % 2 == 0:
            sum += last_digit
        else:
            sum += double_digit(last_digit)

    if sum % 10 > 0:
        return False

    return True


def get_credit_card():
    while True:
        try:
            credit_card = int(input("Number: "))
            return credit_card
        except ValueError:
            pass


def main():
    credit_card = get_credit_card()
    if validate_credit_card(credit_card) == False:
        print("INVALID")
    else:
        indetify_credit_card(credit_card)


if __name__ == "__main__":
    main()
