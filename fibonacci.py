




a, b = 0, 1
sum = 0
for i in range(50):
    a, b = b, a + b
    sum += a
print(sum)
