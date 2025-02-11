def gen():
    n = 1
    yield n

    n += 1
    yield n

    n += 1
    yield n


if __name__ == '__main__':
    a = gen()
    print(a)
    for i in a:
        print(i)
