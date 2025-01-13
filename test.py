from app.models.sql_injection_model import SQLInjectionModel
from flask import Flask, render_template, request
import json
app = Flask(__name__, static_folder="app/static", template_folder="app")
@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
      sql_model = SQLInjectionModel()
      query = request.form['sql_query']
      prediction = sql_model.predict(query)
      return render_template("index.html", prediction = str(prediction), query = query)
    else :
      return render_template("index.html", prediction = None, query = None)

if __name__ == '__main__':
  app.run(debug=True)