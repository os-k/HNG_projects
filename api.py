from flask import Flask, jsonify, request
import datetime

app = Flask(__name__)

@app.route("/api")
def api_endpoint(): 
    slack_name = request.args.get('slack_name')
    track = request.args.get('track')

    if not slack_name:
        return jsonify({"error": "slack_name is required"}), 400
    if not track:
        return jsonify({"error": "track is required"}), 400
    
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    current_day_of_week = days_of_week[datetime.datetime.utcnow().weekday()]

    current_utc_time = datetime.datetime.utcnow()
    current_utc_time_str = current_utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    github_file_url = "https://github.com/os-k/HNG_projects/blob/main/api.py"
    github_repo_url = "https://github.com/os-k/HNGprojects.git"


    user_data = {
        "slack_name": slack_name,
        "current_day_of_week": current_day_of_week,
        "current_utc_time": current_utc_time_str,
        "track": track,
        "github_file_url": github_file_url,
        "github_repo_url": github_repo_url,
        "status_code": 200
    }

    return jsonify(user_data), 200
    
if __name__ == "__main__":
    app.run(debug=True)
