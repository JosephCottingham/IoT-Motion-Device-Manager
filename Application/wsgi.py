from IoT_Manager import app
import os, json
from dotenv import load_dotenv

if __name__ == "__main__":
   # START APP
   load_dotenv()
   app.run(debug=os.environ.get('DEBUG'), port=os.environ.get('PORT'))