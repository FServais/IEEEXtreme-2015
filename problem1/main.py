
while True:
    A0 = input()
    if A0 == "END": break

    i = 1
    A_prec = A0
    A_cur = str(len(A0))
    while A_prec != A_cur:
        i += 1

        A_prec, A_cur = A_cur, str(len(A_cur))

        print("A_prec = {}, A_cur = {}".format(A_prec, A_cur))

    print(i)