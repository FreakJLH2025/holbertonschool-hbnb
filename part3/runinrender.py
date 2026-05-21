import os
from app import create_app, db

config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

print("Current directory:", os.getcwd())
print("Files here:", os.listdir('.'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
