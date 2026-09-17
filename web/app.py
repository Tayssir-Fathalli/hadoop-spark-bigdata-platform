from flask import Flask, render_template
import json

app = Flask(__name__)

def get_kpi1():
    return {"labels": ["Malades", "Sains"], "values": [526, 499]}

def get_kpi2():
    return {"labels": ["Malades", "Sains"], "values": [52.41, 56.57]}

def get_kpi3():
    return {
        "labels": ["Femmes Saines", "Femmes Malades", "Hommes Sains", "Hommes Malades"],
        "values": [86, 226, 413, 300]
    }

def get_kpi4():
    return {
        "labels": ["moins de 40", "40-49", "50-59", "60 et plus"],
        "values": [213.42, 235.05, 248.05, 257.61]
    }

def get_kpi5():
    return {
        "labels": ["Malades", "Sains"],
        "freq": [158.59, 139.13],
        "tension": [129.25, 134.11]
    }

def get_kpi6():
    return {
        "labels": ["Type 0", "Type 1", "Type 2", "Type 3"],
        "sains": [375, 33, 65, 26],
        "malades": [122, 134, 219, 51]
    }

def get_kpi7():
    return {
        "labels": ["Femme <40", "Femme 40-49", "Femme 50-59", "Femme 60+",
                   "Homme <40", "Homme 40-49", "Homme 50-59", "Homme 60+"],
        "taux": [72.4, 85.7, 75.0, 70.0, 38.0, 55.0, 45.0, 40.0]
    }

def get_kpi8():
    return {
        "labels": ["Tres basse (<120)", "Basse (120-139)",
                   "Normale (140-159)", "Elevee (160-179)", "Tres elevee (180+)"],
        "taux_maladie": [25.0, 35.0, 48.0, 62.0, 75.0],
        "total": [20, 85, 210, 450, 260]
    }

@app.route('/')
def index():
    return render_template('index.html',
        kpi1=json.dumps(get_kpi1()),
        kpi2=json.dumps(get_kpi2()),
        kpi3=json.dumps(get_kpi3()),
        kpi4=json.dumps(get_kpi4()),
        kpi5=json.dumps(get_kpi5()),
        kpi6=json.dumps(get_kpi6()),
        kpi7=json.dumps(get_kpi7()),
        kpi8=json.dumps(get_kpi8()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
