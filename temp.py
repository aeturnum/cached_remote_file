def r(f, n):
    offset = f.tell()
    data = f.read(n)
    print '[{}, {}] -> {}'.format(offset, n, data)

f = open('./test_data/data', 'r')
        #         0123456789
r(f, 1) # 0, 1 -> 0
r(f, 1) # 1, 1 ->  1
r(f, 1) # 2, 1 ->   2
f.close()
f = open('./test_data/data', 'r')
        #         0123456789
r(f, 2) # 0, 2 -> 01
r(f, 2) # 2, 2 ->   23
r(f, 2) # 4, 2 ->     45
f.close()

f = open('./test_data/data', 'r')
        #         0123456789
r(f, 3) # 0, 3 -> 012
r(f, 3) # 3, 3 ->    345
r(f, 3) # 6, 3 ->       678 
f.close()