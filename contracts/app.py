from flask import Flask, render_template, request, jsonify
from docxtpl import DocxTemplate
import os
import subprocess
import sqlite3
import json
from dotenv import load_dotenv

app = Flask(__name__)
DOWNLOAD_FOLDER = os.path.join(app.root_path, 'static', 'downloads')
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

load_dotenv()

@app.route("/")
def index():
    try:
        db_path = './static/db/qi.db'
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(f"select id, name from dealers")
        data = cur.fetchall()
        response = [dict(row) for row in data]
        print(response)
    except sqlite3.Error as e:
        print(f"DB insert error {e}")
    finally:
        if conn:
            conn.close()
    return render_template("home.html", data=response)

@app.route("/contract")
def contract():
    if request.method == 'POST':
        print(request.data)
    return render_template("form.html")

@app.route('/get_data', methods=['POST'])
def get_data():
    if request.method == 'POST':
        form_data = dict(request.form)
        print(form_data)
    data = {
        'company_name': form_data['company_name'],
        'full_name': form_data['full_name'],
        'address_1': form_data['address_1'],
        'primary_number': form_data['primary_number'],
        'secondary_number': form_data['secondary_number'],
        'abn_number': form_data['abn_number'],
        'distance_covered': form_data['distance_covered'],
        'standard_inspection': form_data['standard_inspection'],
        'suburbs_list': form_data['suburbs_list'],
        'contract_date': form_data['contract_date']
    }
    template_path = 'template.docx'
    name = data['full_name']
    # file_name, output_pdf = (None, None)
    file_name, output_pdf = fill_contract(template_path, name, data)
    return render_template("download.html", doc_name=f'downloads/{file_name}', pdf_name=f'downloads/{output_pdf}')


@app.route("/invoice")
def invoice_form():
    if request.method == 'POST':
        print(request.data)
    return render_template("invoice.html")


@app.route("/generate_invoice", methods=['POST'])
def generate_invoice():
    if request.method == 'POST':
        items = []
        subtotal = 0
        desc_list = request.form.getlist('description[]')
        qty_list = request.form.getlist('qty[]')
        price_list = request.form.getlist('price[]')
        travel_exp_required = request.form.get('travel_expense_required')
        print(travel_exp_required, "travel_exp_required")
        travel_expense = int(request.form.get('travel_expense') or '0')
        for desc, qty, price in zip(desc_list, qty_list, price_list):
            total = int(qty) * float(price)
            items.append({
                'desc': desc,
                'qty': qty,
                'price': price,
                'total': total
            })
            subtotal += total
        subtotal = round(subtotal, 2)
        gst = round((subtotal / 100 ) * 10, 2)
        grand_total = subtotal + gst
        if travel_exp_required:
            grand_total += travel_expense
        payload = {
            'company_name': request.form.get('company_name'),
            'address': request.form.get('address'),
            'abn_number': request.form.get('abn_number'),
            'invoice_date': request.form.get('invoice_date'),
            'invoice_number': request.form.get('invoice_number'),
            'reference': request.form.get('reference'),
            'due_date': request.form.get('due_date'),
            'travel_exp_required': travel_exp_required,
            'travel_expense': travel_expense,
            'items': items,
            'subtotal': subtotal,
            'gst': gst,
            'grand_total': grand_total,

        }
    print(payload)
    template_path = 'tax_invoice_template.docx'
    name = f"INV {payload['invoice_number']} - {payload['invoice_date']}"
    # file_name, output_pdf = (None, None)
    file_name, output_pdf = fill_contract(template_path, name, payload)
    print(file_name, output_pdf)
    return render_template("download.html", doc_name=f'downloads/{file_name}', pdf_name=f'downloads/{output_pdf}')

@app.route("/onboard", methods=['GET', 'POST'])
def onboard():
    if request.method == 'POST':
        try:
            db_path = './static/db/qi.db'
            conn = sqlite3.connect(db_path)
            print(request.method)
            dealer_company_name = request.form.get('company_name')
            dealer_address = request.form.get('address')
            dealer_abn = request.form.get('abn_number')
            cur = conn.cursor()
            data = (dealer_company_name, dealer_address, dealer_abn)
            cur.execute("insert into dealers (name, address, abn) values (?, ?, ?)", data)
            conn.commit()
        except sqlite3.Error as e:
            print(f"DB insert error {e}")
        finally:
            if conn:
                conn.close()
            return render_template('onboard.html', toast='show')
    return render_template('onboard.html', toast='')



@app.route("/read_data/<int:id>", methods=['GET'])
def read_data(id):
    try:
        db_path = './static/db/qi.db'
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(f"select * from dealers where id = {id}")
        data = cur.fetchall()
        response = [dict(row) for row in data]
    except sqlite3.Error as e:
        print(f"DB insert error {e}")
    finally:
        if conn:
            conn.close()
    return json.dumps(response)

@app.route("/update_dealer", methods=['POST'])
def update_dealer():
    try:
        data = request.get_json()
        id = data['id']
        name = data['name']
        address = data['address']
        abn = data['abn']
        db_path = './static/db/qi.db'
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(f"update dealers set name = '{name}', address = '{address}', abn = '{abn}' where id = {id}")
        conn.commit()
    except sqlite3.Error as e:
        print(f"DB dealer update error {e}")
    finally:
        if conn:
            conn.close()
    return json.dumps({'status': 'ok'})

@app.route("/delete_dealer/<int:id>", methods=['GET'])
def delete_dealer(id):
    try:
        db_path = './static/db/qi.db'
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(f"delete from dealers where id = {id}")
        conn.commit()
    except sqlite3.Error as e:
        print(f"DB insert error {e}")
    finally:
        if conn:
            conn.close()
    return json.dumps({'status': 'ok'})

@app.route("/get_invoice_id", methods=['GET', 'POST'])
def get_invoice_id():
    db_path = './static/db/qi.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    if request.method == 'GET':
        try:
            cur.execute(f"select * from invoice_counter")
            data = cur.fetchone()
            print(data)
        except sqlite3.Error as e:
            print(f"DB insert error {e}")
        finally:
            if conn:
                conn.close()
        return json.dumps({'id': str(data[0]).zfill(5)})
    if request.method == 'POST':
        try:
            cur.execute("update invoice_counter set id = id + 1")
            conn.commit()
        except sqlite3.Error as e:
            print(f"DB insert error {e}")
        finally:
            if conn:
                conn.close()
        return {"status": 200}

@app.route('/verify_key', methods=['POST'])
def verify_key():
    data = request.get_json()
    print(data)
    user_key = data.get('key', '')
    print(user_key, 'user_key')
    if user_key == os.getenv('ACCESS_KEY'):
        return jsonify(success=True)
    return jsonify(success=False)


def fill_contract(template_path, name, payload):
    doc_name = f'{name}.docx'
    output_path = os.path.join(app.config['DOWNLOAD_FOLDER'], doc_name)
    output_pdf = f'{name}.pdf'
    output_path_pdf = os.path.join(app.config['DOWNLOAD_FOLDER'])
    doc = DocxTemplate(template_path)
    doc.render(payload)
    doc.save(output_path)
    subprocess.run(['/usr/bin/soffice',
    '-env:UserInstallation=file:///tmp/LibreOffice_Conversion_${USER}',
    '--headless',
    '--convert-to',
    'pdf:writer_pdf_Export',
    output_path,
    '--outdir',
    output_path_pdf],
    capture_output=True,
    text=True)
    return (doc_name, output_pdf)


if __name__ == '__main__':
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)