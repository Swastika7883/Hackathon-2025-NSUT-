from flask import Flask, render_template, send_file
import csv

app = Flask(__name__)
csv_file = "patientdata.csv.txt"

@app.route('/admin')
def admin_panel():
    records = []
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            records.append(row)
    return render_template('admin.html', records=records)


if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Run this on a different port if needed
