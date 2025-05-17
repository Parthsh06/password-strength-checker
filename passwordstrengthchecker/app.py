from flask import Flask, render_template, request

app = Flask(__name__)

def load_common_passwords():
    try:
        with open("wordlist.txt", "r") as f:
            return set(p.strip().lower() for p in f.readlines())
    except FileNotFoundError:
        return set()

COMMON_PASSWORDS = load_common_passwords()

def check_password_strength(password):
    score = 0
    suggestions = []

    if password.lower() in COMMON_PASSWORDS:
        return "Weak", ["Password is too common. Choose a unique one."]

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters.")

    if any(c.isupper() for c in password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    if any(c.islower() for c in password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        suggestions.append("Include numbers.")

    if any(not c.isalnum() for c in password):
        score += 1
    else:
        suggestions.append("Include special characters.")

    if score >= 6:
        strength = "Strong"
    elif score >= 4:
        strength = "Moderate"
    else:
        strength = "Weak"

    return strength, suggestions

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    suggestions = []
    if request.method == "POST":
        password = request.form["password"]
        result, suggestions = check_password_strength(password)
    return render_template("index.html", strength=result, suggestions=suggestions)

# Required config for Render deployment
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
