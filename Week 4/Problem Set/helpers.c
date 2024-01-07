#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int row = 0; row < height; row++)
    {
        for (int column = 0; column < width; column++)
        {
            int average_color =
                (round(image[row][column].rgbtRed) + round(image[row][column].rgbtGreen) + round(image[row][column].rgbtBlue)) /
                    3.0 +
                0.5;
            image[row][column].rgbtRed = average_color;
            image[row][column].rgbtGreen = average_color;
            image[row][column].rgbtBlue = average_color;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int row = 0; row < height; row++)
    {
        for (int column = 0; column < width / 2; column++)
        {
            RGBTRIPLE temp = image[row][column];

            image[row][column] = image[row][width - column - 1];
            image[row][width - column - 1] = temp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    for (int row = 0; row < height; row++)
    {
        for (int column = 0; column < width; column++)
        {
            temp[row][column] = image[row][column];
        }
    }

    for (int row = 0; row < height; row++)
    {
        for (int column = 0; column < width; column++)
        {
            float iterator = 0.0;
            int avarage_red = 0;
            int avarage_green = 0;
            int avarage_blue = 0;

            for (int x = -1; x < 2; x++)
            {
                for (int y = -1; y < 2; y++)
                {
                    int actual_row = row + x;
                    int actual_column = column + y;

                    if (actual_row < 0 || actual_row > (height - 1) || actual_column < 0 || actual_column > (width - 1))
                    {
                        continue;
                    }

                    avarage_red += image[actual_row][actual_column].rgbtRed;
                    avarage_green += image[actual_row][actual_column].rgbtGreen;
                    avarage_blue += image[actual_row][actual_column].rgbtBlue;

                    iterator++;
                }
            }

            avarage_red = round(avarage_red / iterator);
            avarage_green = round(avarage_green / iterator);
            avarage_blue = round(avarage_blue / iterator);

            temp[row][column].rgbtRed = avarage_red;
            temp[row][column].rgbtGreen = avarage_green;
            temp[row][column].rgbtBlue = avarage_blue;
        }
    }

    for (int row = 0; row < height; row++)
    {
        for (int column = 0; column < width; column++)
        {
            image[row][column] = temp[row][column];
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    for (int row = 0; row < height; row++)
    {
        for (int column = 0; column < width; column++)
        {
            temp[row][column] = image[row][column];
        }
    }

    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    for (int row = 0; row < height; row++)
    {
        for (int column = 0; column < width; column++)
        {
            int red_position[] = {0, 0};
            int green_position[] = {0, 0};
            int blue_position[] = {0, 0};

            for (int x = 0; x < 3; x++)
            {
                for (int y = 0; y < 3; y++)
                {
                    int actual_row = row + x - 1;
                    int actual_column = column + y - 1;

                    if (actual_row < 0 || actual_row > (height - 1) || actual_column < 0 || actual_column > (width - 1))
                    {
                        continue;
                    }

                    red_position[0] = red_position[0] + (image[actual_row][actual_column].rgbtRed * Gx[x][y]);
                    green_position[0] = green_position[0] + (image[actual_row][actual_column].rgbtGreen * Gx[x][y]);
                    blue_position[0] = blue_position[0] + (image[actual_row][actual_column].rgbtBlue * Gx[x][y]);

                    red_position[1] = red_position[1] + (image[actual_row][actual_column].rgbtRed * Gy[x][y]);
                    green_position[1] = green_position[1] + (image[actual_row][actual_column].rgbtGreen * Gy[x][y]);
                    blue_position[1] = blue_position[1] + (image[actual_row][actual_column].rgbtBlue * Gy[x][y]);
                }
            }

            int red = round(sqrt((red_position[0] * red_position[0]) + (red_position[1] * red_position[1])));
            int green = round(sqrt((green_position[0] * green_position[0]) + (green_position[1] * green_position[1])));
            int blue = round(sqrt((blue_position[0] * blue_position[0]) + (blue_position[1] * blue_position[1])));

            if (red > 255)
            {
                red = 255;
            }

            if (green > 255)
            {
                green = 255;
            }

            if (blue > 255)
            {
                blue = 255;
            }

            temp[row][column].rgbtRed = red;
            temp[row][column].rgbtGreen = green;
            temp[row][column].rgbtBlue = blue;
        }
    }

    for (int row = 0; row < height; row++)
    {
        for (int column = 0; column < width; column++)
        {
            image[row][column] = temp[row][column];
        }
    }

    return;
}
