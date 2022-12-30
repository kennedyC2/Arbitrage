# Import Dependencies
# ==============================================================================
from flask import Flask, jsonify, request, render_template, make_response, send_file, redirect
import json
import ssl
from waitress import serve

# Instantiate
# ==============================================================================
app = Flask(__name__)

# Https
# ==============================================================================
# context = ssl.SSLContext(ssl.PROTOCOL_TLS)
# context.load_cert_chain("./https/cert.pem", "./https/key.pem")


# Enforce HTTPS
# ==============================================================================
# @app.before_request
# def checkProtocol():
#     if not request.is_secure:
#         url = request.url.replace("http://", "https://")
#         return redirect(url, code=302)


# ==============================================================================
#                                ROUTES
# ==============================================================================


# App
# ==============================================================================
@app.route("/", methods=["GET"])
def home():
    if request.method == "GET":
        return render_template("app.html")
    return


# Get Favicon
# ==============================================================================
@app.route("/favicon.ico", methods=["GET"])
def favicon():
    if request.method == "GET":
        return send_file("./favicon/favicon.ico")
    return


@app.route("/favicon-32x32.png", methods=["GET"])
def favicon32():
    if request.method == "GET":
        return send_file("./favicon/favicon-32x32.png")
    return

# Get Background
# ==============================================================================


@app.route("/images/pexels-eberhard-grossgasteiger-691668.jpg", methods=["GET"])
def background():
    if request.method == "GET":
        return send_file("./images/pexels-eberhard-grossgasteiger-691668.jpg")
    return


# Get 3-way
# ==============================================================================
@app.route("/3way", methods=["GET"])
def arb3():
    if request.method == "GET":
        with open('C:/Software Development/Arbitrage/arb3.txt', 'r') as outfile:
            return jsonify(
                json.load(outfile))
    return


if __name__ == '__main__':
    # app.run(host="127.0.0.1", port=5000, debug=True, ssl_context=context)
    serve(app, host="127.0.0.1", port=4090, url_scheme="https")
