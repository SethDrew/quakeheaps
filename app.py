import sys
sys.path.append("lib/")
from flask import Flask
from flask import render_template
import json

app = Flask(__name__)

@app.route("/")
def index():
    with open("./static/tree_data.json") as f:
        tree_json = json.load(f)
    print(tree_json)
    return render_template("treeview.html", tree_json=tree_json)


if __name__ == "__main__":
    app.run(debug=True, port=8000)

