T = int(input())

for _ in range(0, T):
    inp = list(map(int, input().split(" ")))
    n_participants = inp[0]
    c = inp[1]

    predictions = {}
    for _ in range(0,n_participants):
        name = input()

        predict_values = []
        for _ in range(0,c):
            p = list(map(int, input().split(" ")))
            predict_values.append((p[0], p[1]))

        predictions[name] = predict_values

    real = []
    for _ in range(0,c):
        s = input().split(" ")
        if s[0] != "?" and s[1] != "?":
            s = list(map(int, s))
        real.append((s[0], s[1]))

    print(predictions)
    print(real)