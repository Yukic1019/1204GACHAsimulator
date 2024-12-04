import os
from flask import Flask, render_template, session, redirect, url_for, request
from gacha import draw_gacha, draw_11_gacha, simulate_until_all_sr_plus

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATAFILE = 'gacha_results.txt'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gacha')
def gacha():
    result = draw_gacha()
    session['results'] = session.get('results', []) + [result]
    session['total'] = session.get('total', 0) + 1
    session['cost'] = session.get('cost', 0) + 100
    session['single_gacha_count'] = session.get('single_gacha_count', 0) + 1

    # 結果をファイルに保存
    with open(DATAFILE, 'a') as f:
        f.write(result + '\n')

    return render_template('gacha.html', result=result)

@app.route('/11gacha')
def gacha_11():
    results = draw_11_gacha()
    session['results'] = session.get('results', []) + results
    session['total'] = session.get('total', 0) + 11
    session['cost'] = session.get('cost', 0) + 1000
    session['multi_gacha_count'] = session.get('multi_gacha_count', 0) + 1

    # 結果をファイルに保存
    with open(DATAFILE, 'a') as f:
        for result in results:
            f.write(result + '\n')

    return render_template('11gacha.html', results=results)

@app.route('/reset')
def reset():
    session['total'] = 0
    session['results'] = []
    session['cost'] = 0
    session['single_gacha_count'] = 0
    session['multi_gacha_count'] = 0

    # ファイルの内容をクリア
    with open(DATAFILE, 'w') as f:
        f.write('')

    return redirect(url_for('index'))

@app.route('/total')
def total():
    total = session.get('total', 0)
    results = session.get('results', [])
    cost = session.get('cost', 0)
    single_gacha_count = session.get('single_gacha_count', 0)
    multi_gacha_count = session.get('multi_gacha_count', 0)

    # 各レアリティのカウント
    counts = {'N': 0, 'N+': 0, 'R': 0, 'R+': 0, 'SR': 0, 'SR+': 0}
    for result in results:
        if 'N' in result:
            counts['N'] += 1
        elif 'N+' in result:
            counts['N+'] += 1
        elif 'R' in result:
            counts['R'] += 1
        elif 'R+' in result:
            counts['R+'] += 1
        elif 'SR' in result:
            counts['SR'] += 1
        elif 'SR+' in result:
            counts['SR+'] += 1

    return render_template('total.html', total=total, results=results, cost=cost, counts=counts, single_gacha_count=single_gacha_count, multi_gacha_count=multi_gacha_count)

@app.route('/simulate')
def simulate():
    count, draws = simulate_until_all_sr_plus()

    # 費用計算の修正
    single_gacha_count = sum(1 for draw in draws if draw[0] == 'ガチャ')
    multi_gacha_count = sum(1 for draw in draws if draw[0] == '11連ガチャ')

    cost = single_gacha_count * 100 + multi_gacha_count * 1000

    return render_template('simulate.html', count=count, draws=draws, cost=cost, single_gacha_count=single_gacha_count, multi_gacha_count=multi_gacha_count)

@app.route('/load_results')
def load_results():
    if os.path.exists(DATAFILE):
        with open(DATAFILE, 'r') as f:
            results = f.read().splitlines()
        return render_template('load_results.html', results=results)
    else:
        return "No saved results found."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)