line = "test line for upload check\n"

with open("small.txt", "w") as f:
    while f.tell() < 5120:
        f.write(line)

with open("big.txt", "w") as f:
    while f.tell() < 15360:
        f.write(line)

print("Files created")