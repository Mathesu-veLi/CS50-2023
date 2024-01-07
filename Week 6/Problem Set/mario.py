def print_the_spaces(height_of_pyramid, row_length):
    for spaces in range(0, height_of_pyramid - row_length):
        if spaces != 0:
            print(" ", end="")


def print_a_column(row_length, height_of_pyramid, is_left):
    if is_left:
        print_the_spaces(height_of_pyramid, row_length)

    for column in range(row_length + 1):
        print("#", end="")


def print_pyramid(height_of_pyramid):
    for row in range(height_of_pyramid):
        print_a_column(row, height_of_pyramid, True)

        print("  ", end="")

        print_a_column(row, height_of_pyramid, False)

        print()


def get_height():
    while True:
        try:
            height = int(input("Height: "))
            if height >= 1 and height <= 8:
                return height
        except ValueError:
            pass


def main():
    height = get_height()

    print_pyramid(height)


if __name__ == "__main__":
    main()
