import random

def draw_gacha():
    rarities = ['N', 'N+', 'R', 'R+', 'SR', 'SR+']
    probabilities = [0.40, 0.30, 0.20, 0.09, 0.007, 0.003]
    result = random.choices(rarities, probabilities)[0]

    # 各レアリティ内でランダムにカードを選ぶ
    if result == 'N':
        card = f'N{random.randint(1, 20):02}'
    elif result == 'N+':
        card = f'N+{random.randint(1, 20):02}'
    elif result == 'R':
        card = f'R{random.randint(1, 15):02}'
    elif result == 'R+':
        card = f'R+{random.randint(1, 15):02}'
    elif result == 'SR':
        card = f'SR{random.randint(1, 10):02}'
    elif result == 'SR+':
        card = f'SR+{random.randint(1, 10):02}'

    return card

def draw_11_gacha():
    return [draw_gacha() for _ in range(11)]

def simulate_until_all_sr_plus():
    sr_plus_types = set([f'SR+{i:02}' for i in range(1, 11)])
    obtained = set()
    count = 0
    draws = []
    max_iterations = 100000  # 無限ループを防ぐための最大回数
    iterations = 0

    while obtained != sr_plus_types and iterations < max_iterations:
        if random.random() < 0.5:  # 50%の確率で11連ガチャを引く
            results = draw_11_gacha()
            draws.append(('11連ガチャ', results))
            count += 11
        else:
            result = draw_gacha()
            draws.append(('ガチャ', result))
            count += 1
            results = [result]

        for result in results:
            if result.startswith('SR+'):
                obtained.add(result)

        iterations += 1

    if iterations >= max_iterations:
        print("Warning: Maximum iterations reached. Simulation may not have completed correctly.")

    return count, draws
