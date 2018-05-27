from util.distribution import PoissonProcess

if __name__ == '__main__':
    p = PoissonProcess(3)
    for i in range(10):
        print(p())
