from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

# Fonction pour scraper les conjugaisons
def scrape_conjugations(verb):
    url = f"http://www.les-verbes.com/conjuguer.php?verbe={verb}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    verb_conjugations = {}

    verb_tenses = soup.find_all("div", class_="verbetitle")
    verb_boxes = soup.find_all("div", class_="verbebox")

    for i, tense in enumerate(verb_tenses):
        tense_name = tense.h2.text.strip()
        if i < len(verb_boxes):
            conjugations = verb_boxes[i].p.get_text().strip().split("\n")
            verb_conjugations[tense_name] = conjugations
    
    return verb_conjugations

# Route pour afficher les conjugaisons en JSON via paramètre de requête
@app.route('/conjugaison', methods=['GET'])
def conjugate():
    verb = request.args.get('verbe')  # Obtenir le verbe du paramètre de requête
    if not verb:
        return jsonify({"error": "Aucun verbe fourni"}), 400  # Gérer les erreurs si aucun verbe n'est fourni
    conjugations = scrape_conjugations(verb)
    return jsonify(conjugations)

# Exécuter l'application sur l'host 0.0.0.0 et le port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
