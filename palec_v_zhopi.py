def make_binary(number):
    digits = []
    print(number)
    for _ in range(5):
        number *= 2
        print(number, end=" ")
        if number >= 1:
            number -= 1
            digits.append(1)
        else:
            digits.append(0)
        print(f" {digits[-1]}")

make_binary(0.968447)