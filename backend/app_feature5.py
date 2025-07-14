from flask import Flask, jsonify
import pandas as pd
import os
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

@app.route('/redistribute', methods=['GET'])
def get_suggestions():
    print("Redistribute endpoint hit") 
    filepath = '../data/redistribution_suggestions.csv'

    if not os.path.exists(filepath):
        return jsonify({"error": "redistribution_suggestions.csv not found"}), 404

    try:
        df = pd.read_csv(filepath)
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,port=5001)
