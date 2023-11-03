




from collections import Counter

from statistics import mean

from statistics import median

from statistics import mode

from statistics import variance

import psycopg2




# Dataset
colors = ['GREEN', 'YELLOW', 'GREEN', 'BROWN', 'BLUE', 'PINK', 'BLUE', 'YELLOW', 'ORANGE', 'CREAM', 'ORANGE', 'RED', 'WHITE', 'BLUE', 'WHITE', 'BLUE', 'BLUE', 'BLUE', 'GREEN',
          'ASH', 'BROWN', 'GREEN', 'BROWN', 'BLUE', 'BLUE', 'BLUE', 'PINK', 'PINK', 'ORANGE', 'ORANGE', 'RED', 'WHITE', 'BLUE', 'WHITE', 'WHITE', 'BLUE', 'BLUE', 'BLUE',
          'GREEN', 'YELLOW', 'GREEN', 'BROWN', 'BLUE', 'PINK', 'RED', 'YELLOW', 'ORANGE', 'RED', 'ORANGE', 'RED', 'BLUE', 'BLUE', 'WHITE', 'BLUE', 'BLUE', 'WHITE', 'WHITE',
          'BLUE', 'BLUE', 'GREEN', 'WHITE', 'BLUE', 'BROWN', 'PINK', 'YELLOW', 'ORANGE', 'CREAM', 'ORANGE', 'RED', 'WHITE', 'BLUE', 'WHITE', 'BLUE', 'BLUE', 'BLUE', 'GREEN',
          'GREEN', 'WHITE', 'GREEN', 'BROWN', 'BLUE', 'BLUE', 'BLACK', 'WHITE', 'ORANGE', 'RED', 'RED', 'RED', 'WHITE', 'BLUE', 'WHITE', 'BLUE', 'BLUE', 'BLUE', 'WHITE']


# Assign numerical values to colors
color_values = {
    'GREEN': 1,
    'YELLOW': 2,
    'BROWN': 3,
    'BLUE': 4,
    'PINK': 5,
    'ORANGE': 6,
    'CREAM': 7,
    'RED': 8,
    'WHITE': 9,
    'BLACK': 10,
    'ASH': 11
}


# Frequency of each color in the dataset
frequency = Counter(colors)



# Interpret the colors in the dataset into numerical data
numerical_values = [color_values[color] for color in colors]

# Arranging the numerical data in ascending order
sorted_colors = [color for color in sorted(numerical_values)]



# Calculate the mean color value
mean_color_value = mean(sorted_colors)

# Find the corresponding color for the mean color value
mean_color = next(color for color, value in color_values.items() if value == round(mean_color_value))

print('The mean color is', mean_color)

# Calculate the most color worn throughout the week(mode)
mode_color_value = mode(sorted_colors)

# Find the corresponding color for the mode color value
most_common_color = next(color for color, value in color_values.items() if value == round(mode_color_value))


print(most_common_color, 'is the color worn mostly throughout the week,', frequency.most_common(1)[0][1], 'times')


# Calculate the median color value
median_color_value = median(sorted_colors)


# Find the corresponding color for the median color value
median_color = next(color for color, value in color_values.items() if value == round(median_color_value))

print(median_color, 'is the median color')


# Calculate the variance color value
variance_color_value = variance(sorted_colors)

# Find the corresponding color for the variance color value
variance_color = next(color for color, value in color_values.items() if value == round(variance_color_value))

print(variance_color, 'is the variance of the colors')


# Calculate the probability that a color chosen at random is red
red_probability = (sorted_colors.count(8))/(len(sorted_colors))

print("If a color is chosen at random, the probability that the color is red is", red_probability)




# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(
        host="localhost",
        database="colors",
        user="root",
        password="mYrootpa649sSword"
    )
    cur = conn.cursor()

    # Insert data into the PostgreSQL database
    for color, freq in frequency.items():
        cur.execute("INSERT INTO color_frequencies (color, frequency) VALUES (%s, %s)", (color, freq))

    conn.commit()

    print("Update successful!")

    cur.close()
    conn.close()

except Exception as e:
    print("Error: Update not successful")








