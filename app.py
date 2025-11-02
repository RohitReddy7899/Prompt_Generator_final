from flask import Flask, render_template
from routes.composer_routes import composer_bp
from routes.library_routes import library_bp

app = Flask(__name__)
app.register_blueprint(composer_bp)
app.register_blueprint(library_bp)

@app.route('/')
def home():
    return render_template('composer.html')

if __name__ == '__main__':
    app.run(debug=True)
