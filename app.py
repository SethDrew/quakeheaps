import sys
sys.path.append("lib/")
from flask import Flask
from flask import render_template, request, jsonify

from gen import create_heap, update_heap, extract_min, decrease_key, run_quake


import json

app = Flask(__name__)

@app.route("/")
def index():
    # with open("./static/tree_data.json") as f:
    #     tree_json = json.load(f)
    # print(tree_json)
    tree_json = create_heap(0)

    return render_template("treeview.html", tree_json=tree_json)

@app.route("/update")
def update():
    num = int(request.args.get('num'))
    return jsonify(update_heap(num)['all'])

@app.route("/extract")
def extract():
    m, dump, quake_level = extract_min()
    return jsonify({'min': m, 'all':dump['all'], 'quake_level':quake_level})

@app.route("/quake")
def quake():
    dump, quake_level = run_quake()
    
    return jsonify({'all':dump['all'], 'quake_level':quake_level})

@app.route("/decrease")
def decrease():
    node = int(request.args.get('node'))
    k, dump = decrease_key(node)
    return jsonify({"newkey": k, "all":dump['all']})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
