import random

def draw_gacha():
    rarities = ['N', 'N+', 'R', 'R+', 'SR', 'SR+']
    probabilities = [0.33, 0.25, 0.20, 0.15, 0.05, 0.02]
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
    results = []
    for _ in range(10):
        rarities = ['R', 'R+', 'SR', 'SR+']
        probabilities = [0.57, 0.30, 0.10, 0.03]
        result = random.choices(rarities, probabilities)[0]

        # 各レアリティ内でランダムにカードを選ぶ
        if result == 'R':
            card = f'R{random.randint(1, 15):02}'
        elif result == 'R+':
             card = f'R+{random.randint(1, 15):02}'
        elif result == 'SR':
            card = f'SR{random.randint(1, 10):02}'
        elif result == 'SR+':
            card = f'SR+{random.randint(1, 10):02}'
        results.append(card)

    # 11回目の結果は必ずSRにする
    card = f'SR{random.randint(1, 10):02}'
    results.append(card)
    return results

def simulate_until_all_sr_plus():
    sr_plus_types = set([f'SR+{i:02}' for i in range(1, 11)])
    obtained = set()
    count = 0
    draws = []
    max_iterations = 10000  # 無限ループを防ぐための最大回数
    iterations = 0

    while obtained != sr_plus_types and iterations < max_iterations:
        results = draw_11_gacha()
        draws.append(('11連ガチャ', results))
        count += 11

        for result in results:
            if result.startswith('SR+'):
                obtained.add(result)

        iterations += 1

    if iterations >= max_iterations:
        print("Warning: Maximum iterations reached. Simulation may not have completed correctly.")

    return count, draws