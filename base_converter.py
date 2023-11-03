
import random



# Generate a four digit random binary number
binary = ""
for i in range(4):
    binary += str(random.randint(0,1))


# Convert the binary number to decimal
decimal = 0
for digit in binary:
    decimal = decimal * 2 + int(digit)

print(binary, "in decimal is:", decimal)