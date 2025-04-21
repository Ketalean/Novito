with open('./static/save_images/num.txt') as f:
    n = int(f.readline())
    n += 1
    with open('./static/save_images/num.txt', 'w') as file:
        file.write(str(n))

