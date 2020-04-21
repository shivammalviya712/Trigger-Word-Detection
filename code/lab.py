"""All the crazy ideas are tested here."""

def temper(y):
    y_len = len(y)
    for i in range(0, y_len):
        y[i][0] = 1


y = [[0], [0], [0], [0], [0]]
print(y[3][0])
temper(y)
print(y)