from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import socket
from datetime import datetime
import subprocess

app = Flask(__name__)
CORS(app) 

client = MongoClient("mongodb://localhost:27017/")  
db = client["twitter_data"]
collection = db["trending_topics"]


@app.route('/run_script', methods=['GET'])
def run_script():
    try:
    
        result = subprocess.run(['python', 'main.py'], capture_output=True, text=True)
 
        if result.returncode != 0:
            return jsonify({"error": f"Error: {result.stderr}"}), 500
  
        return jsonify({"message": f"Script executed successfully. Output: {result.stdout}"}), 200
    
    except Exception as e:
        return jsonify({"error": f"Error executing script: {str(e)}"}), 500
    
    
@app.route('/get_trending_data', methods=['GET'])
def get_trending_data():
    try:
        # Retrieve the latest trending data from MongoDB
        trending_data = collection.find_one({}, sort=[("date_time", -1)])  # Get the most recent data
        if trending_data:
            trending_data["_id"] = str(trending_data["_id"])  # Convert ObjectId to string
            trending_data["date_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            trending_data["ip_address"] = socket.gethostbyname(socket.gethostname())
            
            return jsonify(trending_data)

        else:
            return jsonify({"error": "No trending data found."})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    
    
    
    



