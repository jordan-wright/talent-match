from talent_match import app, db
from config import basedir
import os.path

# Create the db if it doesn't exist
if not os.path.exists(os.path.join(basedir, 'talent_match.db')):
	print "Creating database..."
	db.create_all()

app.run(debug=True)
