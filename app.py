import os
import random
from flask import Flask, render_template, request, jsonify

# Render'ın klasör yolunu sorunsuz bulması için mutlak yol tanımı
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
app = Flask(__name__, template_folder=template_dir)

# Oyun durumu için sözlük
oyun_verisi = {
    "tutulan_sayi": random.randint(1, 100),
    "tahmin_sayisi": 0
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tahmin', methods=['POST'])
def tahmin():
    try:
        veri = request.get_json()
        kullanici_tahmini = int(veri['tahmin'])
    except (TypeError, ValueError):
        return jsonify({"sonuc": "Lütfen geçerli bir sayı girin!", "durum": "hata"})

    oyun_verisi["tahmin_sayisi"] += 1
    sayi = oyun_verisi["tutulan_sayi"]
    deneme = oyun_verisi["tahmin_sayisi"]

    if kullanici_tahmini < sayi:
        return jsonify({"sonuc": "Daha buyuk bir sayi soyle!", "durum": "kucuk", "deneme": deneme})
    elif kullanici_tahmini > sayi:
        return jsonify({"sonuc": "Daha kucuk bir sayi soyle!", "durum": "buyuk", "deneme": deneme})
    else:
        mesaj = f"Tebrikler! {deneme}. denemede bildin!"
        return jsonify({"sonuc": mesaj, "durum": "bildi", "deneme": deneme})

@app.route('/sifirla', methods=['POST'])
def sifirla():
    oyun_verisi["tutulan_sayi"] = random.randint(1, 100)
    oyun_verisi["tahmin_sayisi"] = 0
    return jsonify({"sonuc": "Yeni oyun basladi!"})

if __name__ == '__main__':
    app.run(debug=True)
