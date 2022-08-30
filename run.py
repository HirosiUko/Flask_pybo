import os
from pybo import create_app
port = int(os.environ.get("PORT", 5000))
app = create_app()
app.run(port=port)