from flask import Flask, request
from main import simulate_http

app = Flask(__name__)

#
# Google Cloud Run main entry point
#
@app.route('/', methods=['POST'])
def GC_Run_simulate_http():
    return simulate_http(request)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))