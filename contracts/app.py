from flask import Flask, render_template, request
import os
import subprocess

app = Flask(__name__)
DOWNLOAD_FOLDER = os.path.join(app.root_path, 'static', 'downloads')
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

@app.route("/")
def hello_world():
    if request.method == 'POST':
        print(request.data)
    return render_template("form.html", person='vikky')


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
        company_name = request.form.get('company_name')
        address = request.form.get('address')
        abn_number = request.form.get('abn_number')
        invoice_date = request.form.get('invoice_date')
        invoice_number = request.form.get('invoice_number')
        reference = request.form.get('reference')
        due_date = request.form.get('due_date')
        for desc, qty, price in zip(desc_list, qty_list, price_list):
            total = int(qty) * int(price)
            items.append({
                'desc': desc,
                'qty': qty,
                'price': price,
                'total': total
            })
            subtotal += total
        gst = int((subtotal / 100 ) * 10)
        grand_total = subtotal + gst
        payload = {
            'company_name': company_name,
            'address': address,
            'abn_number': abn_number,
            'invoice_date': invoice_date,
            'invoice_number': invoice_number,
            'reference': reference,
            'due_date': due_date,
            'items': items,
            'subtotal': subtotal,
            'gst': gst,
            'grand_total': grand_total,
            
        }
        print(payload)
    return {'status': 'ok'}

if __name__ == '__main__':
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)