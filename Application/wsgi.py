from IoT_Manager import app
import os, json
from dotenv import load_dotenv

if __name__ == "__main__":
   # LOAD VARIABLES INTO ENVIROMENT
   load_dotenv()
   # START APP
   app.run(debug=os.environ.get('DEBUG'), port=os.environ.get('PORT'))