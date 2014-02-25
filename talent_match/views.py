from talent_match import app

@app.route('/')
def index():
    return 'Hello World!'