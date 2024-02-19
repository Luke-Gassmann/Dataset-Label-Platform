import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
import sys
from flask_wtf.csrf import CSRFProtect
import os.path
import json
import numpy as np

last_id_file_name = "static/Resources/last_id.txt"

def save_last_id(id_):
    with open(last_id_file_name, 'w') as f:
        f.write(str(id_))

def read_last_id():

    if os.path.exists(last_id_file_name):

        with open(last_id_file_name) as f:
            id_ = int(f.read())

    else:
        id_ = 1

    return id_


last_id_file_name_csv_master = "static/Resources/last_id_csv_master.txt"

def save_last_id_csv_master(id_):
    with open(last_id_file_name_csv_master, 'w') as f:
        f.write(str(id_))

def read_last_id_csv_master():

    if os.path.exists(last_id_file_name_csv_master):

        with open(last_id_file_name_csv_master) as f:
            id_ = int(f.read())

    else:
        id_ = 0

    return id_

# Create reviewing page

# 415168

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
crsf = CSRFProtect(app)

@app.route('/', methods=["GET"])
def main():
    return redirect(url_for('csv_master'))


def collect_json_settings():
    with open("settings.json") as json_data:
        data = json.load(json_data)

    return data


def collect_json_combination():
    try:
        with open("static/combination_save.json") as json_data:
            data = json.load(json_data)
    except Exception:
        data = []
    return data

def save_json_combination(json_object):
    with open("static/combination_save.json", 'w') as f:
        json.dump(json_object, f)

@app.route('/csv_master', methods=["POST", "GET"])
def csv_master():

    settings = collect_json_settings()

    stored_combination = collect_json_combination()
    file_name = settings["csv_file_name"]
    df = pd.read_csv(file_name)

    id = request.args.get("id")

    if id is None:
        id = int(read_last_id_csv_master())
    else:
        if int(id) == -1:
            id = len(df) - 1
        elif int(id) == len(df):
            id = 0
        save_last_id_csv_master(int(id))

    print(id, file=sys.stdout)

    if settings["label_column_name"] not in df:
        df[settings["label_column_name"]] = np.nan

    df[settings["label_column_name"]].fillna("None", inplace=True)

    rows_left = len(df.loc[df[settings["label_column_name"]] == "None"])
    rows_done = len(df.loc[df[settings["label_column_name"]] != "None"])

    print(df, file=sys.stdout)

    row = df.loc[int(id)]
    current_label = row[settings["label_column_name"]]


    if str(current_label) == "nan" or current_label == "None":
        current_label = "None"
        stringified_current_label = "None"
    else:
        current_label = json.loads(row[settings["label_column_name"]])
        stringified_current_label = json.dumps(current_label)

    display_data = [[column, column.replace("_", " ").title(), row[column]] for column in settings["display_columns"]]

    return render_template(
        'csv_master.html',
        current_id=id,
        labels=settings["labels"],
        display_columns=settings["display_columns"],
        display_data=display_data,
        current_label=current_label,
        stringified_current_label=stringified_current_label,
        rows_left=rows_left,
        rows_done=rows_done,
        stored_combination=stored_combination,
        file_name=file_name
    )



@app.route('/csv_master_combination_save', methods=["POST"])
def csv_master_combination_save():
    package = {
        "success": False,
        "error": "No Errors"
    }

    try:
        data = request.form
        combination = data.get("combination")

        combination_json = json.loads(combination)
        save_json_combination(combination_json)

        package["success"] = True

    except Exception:
        package["success"] = False
        package["error"] = "Failed to save json"

    return package

@app.route('/row_save_csv_master', methods=["POST"])
def row_save_csv_master():

    package = {
        "success": False,
        "error": "No Errors"
    }

    settings = collect_json_settings()

    df = pd.read_csv(settings["csv_file_name"])

    data = request.form
    id = int(data.get("id"))
    label = str(data.get("label"))

    true_labels = [i[0] for i in settings["labels"]]

    labels_validated = True
    if label != "None":
        print(label, file=sys.stdout)
        json_label = json.loads(label)

        for label_for_validation in json_label:

            if label_for_validation not in true_labels:
                labels_validated = False
                break

    failed = False
    if label == "None":
        label = None
    elif not labels_validated:
        failed = True
        package["error"] = "Invalid Label"

    if not failed:

        df.loc[id, settings['label_column_name']] = label
        df.to_csv(settings["csv_file_name"], index=False)
        package["success"] = True

    return package


if __name__ == '__main__':
    app.run(debug=True)
