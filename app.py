from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import requests
import json
import io
import concurrent.futures
import time
import os

app = Flask(__name__)
CORS(app)

# Developer Information
DEVELOPER_INFO = {
    "name": "Refat Rahman",
    "website": "https://refat.ovh",
    "github": "https://github.com/refatbd",
    "facebook_id": "https://www.facebook.com/rjrefat/",
    "facebook_page": "https://www.facebook.com/fb.refat.ovh",
    "instagram": "https://www.instagram.com/refat_official",
    "telegram": "https://t.me/refatbd",
    "whatsapp": "+8801747032300"
}

AUTHORIZED_TOKENS = {
    "refatbd": "active",
    "refat": "active"
}

BAN_PERIOD_MAP = {
    604800: "7 Days",
    259200: "3 Days",
    86400: "1 Day",
    3600: "1 Hour",
    1800: "30 Minutes",
    600: "10 Minutes",
    0: "Permanent / Not Specified"
}

# ---------------- ROUTES ----------------

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/api", methods=["GET"])
def api_info():
    return jsonify({
        "service": "Free Fire Ban Check API",
        "status": "online",
        "developer": DEVELOPER_INFO
    })

@app.route("/check_key", methods=["GET"])
def verify_key_route():
    token = request.args.get("key", "")
    is_valid, response_data = check_access(token)
    if not is_valid:
        return jsonify(response_data)
    return jsonify({"status": "valid", "key_status": AUTHORIZED_TOKENS.get(token)})

@app.route("/bancheck", methods=["GET"])
def check_player_ban():
    token = request.args.get("key", "")
    target_uid = request.args.get("uid", "")

    is_valid, auth_response = check_access(token)
    if not is_valid:
        return jsonify(auth_response)
    if not target_uid:
        return jsonify({"error": "Player ID (uid) is required", "status_code": 400})

    return jsonify(fetch_garena_data(target_uid))

# ---------------- CORE FUNCTION ----------------

def fetch_garena_data(uid):
    api_url = f"https://ff.garena.com/api/antihack/check_banned?lang=en&uid={uid}"
    req_headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "referer": "https://ff.garena.com/en/support/",
        "x-requested-with": "B6FksShzIgjfrYImLpTsadjS86sddhFH"
    }

    try:
        res = requests.get(api_url, headers=req_headers, timeout=10)
        if res.status_code == 200:
            parsed_data = res.json().get("data", {})
            banned_status = parsed_data.get("is_banned", 0)
            ban_duration = parsed_data.get("period", 0)

            is_7_day_ban = (banned_status == 1 and ban_duration == 604800)
            readable_period = BAN_PERIOD_MAP.get(ban_duration, f"{ban_duration} seconds")

            return {
                "uid": uid,
                "is_banned": bool(banned_status),
                "status": "BANNED" if banned_status else "NOT BANNED",
                "ban_period_seconds": ban_duration if banned_status else 0,
                "ban_period_readable": readable_period if banned_status else "N/A",
                "is_7_day_ban": is_7_day_ban,
                "ban_type": "7 Days Ban" if is_7_day_ban else ("Other Ban" if banned_status else "No Ban")
            }
        else:
            return {"uid": uid, "error": "Failed to fetch", "status_code": 500}
    except Exception as e:
        return {"uid": uid, "error": str(e), "status_code": 500}

# ---------------- BULK CHECK ----------------

@app.route("/bulk_check", methods=["POST"])
def bulk_check():
    token = request.form.get("key", "") or request.args.get("key", "")
    is_valid, auth_response = check_access(token)
    if not is_valid:
        return jsonify(auth_response), 401

    # --- JSON body (direct text) ---
    data = None
    if request.is_json:
        data = request.get_json()
    # --- File upload ---
    elif "file" in request.files:
        file = request.files["file"]
        try:
            data = json.load(file)
        except Exception as e:
            return jsonify({"error": f"Invalid JSON file: {str(e)}"}), 400
    # --- Raw text form ---
    elif "json_data" in request.form:
        try:
            data = json.loads(request.form["json_data"])
        except Exception as e:
            return jsonify({"error": f"Invalid JSON text: {str(e)}"}), 400
    else:
        return jsonify({"error": "No JSON data provided"}), 400

    # --- Extract UIDs ---
    if not isinstance(data, list):
        return jsonify({"error": "JSON must be a list of objects"}), 400

    uids = []
    for item in data:
        if isinstance(item, dict):
            if "uid" in item:
                uids.append(str(item["uid"]).strip())
        elif isinstance(item, str) or isinstance(item, int):
            uids.append(str(item).strip())

    if not uids:
        return jsonify({"error": "No valid UIDs found in JSON"}), 400

    # --- Parallel check with max 20 workers ---
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_uid = {executor.submit(fetch_garena_data, uid): uid for uid in uids}
        for future in concurrent.futures.as_completed(future_to_uid):
            results.append(future.result())

    # --- Split into banned / not banned / errors ---
    banned = [r for r in results if r.get("is_banned")]
    not_banned = [r for r in results if not r.get("is_banned") and "error" not in r]
    errors = [r for r in results if "error" in r]
    seven_day_bans = [r for r in banned if r.get("is_7_day_ban")]

    return jsonify({
        "total": len(uids),
        "banned_count": len(banned),
        "not_banned_count": len(not_banned),
        "error_count": len(errors),
        "seven_day_ban_count": len(seven_day_bans),
        "banned": banned,
        "not_banned": not_banned,
        "seven_day_bans": seven_day_bans,
        "errors": errors
    })

# ---------------- DOWNLOAD RESULT ----------------

@app.route("/download_result", methods=["POST"])
def download_result():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400

    output = io.BytesIO()
    output.write(json.dumps(data, indent=2).encode("utf-8"))
    output.seek(0)

    return send_file(
        output,
        mimetype="application/json",
        as_attachment=True,
        download_name=f"ff_ban_result_{int(time.time())}.json"
    )

# ---------------- AUTH ----------------

def check_access(token):
    if not token:
        return False, {"error": "API key is missing", "status_code": 401}
    if token not in AUTHORIZED_TOKENS:
        return False, {"error": "Invalid API key", "status_code": 401}
    state = AUTHORIZED_TOKENS[token]
    if state == "inactive":
        return False, {"error": "API key is inactive", "status_code": 403}
    if state == "banned":
        return False, {"error": "API key is banned", "status_code": 403}
    return True, {"valid": True}

@app.route("/developer", methods=["GET"])
def developer():
    return jsonify({"developer": DEVELOPER_INFO})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)