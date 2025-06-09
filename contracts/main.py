from docx import Document

def fill_contract(template_path, output_path, data):
    doc = Document(template_path)

    for paragraph in doc.paragraphs:
        for key, value in data.items():
            if key in paragraph.text:
                for run in paragraph.runs:
                    run.text = run.text.replace(key, value)
    doc.save(output_path)


if __name__ == '__main__':
    data = {
        '[company_name]': 'Dummy Company Pty Ltd',
        '[full_name]': 'Dummy Name',
        '[address_1]': 'Dummy Street',
        '[address_2]': 'Dummy Street 2, Vic',
        '[phone_number]': '1234567890',
        '[abn_number]': '1234567890',
        '[distance_covered]': '10',
        '[standard_inspection]': 'Lorem ipsum',
        '[outside_suburbs_charge]': '10',
        '[suburbs_list]': 'big comma sperarted values',
        '[account_name]': 'Dummy Bank',
        '[bsb]': '12345',
        '[account_number]': '1234567890',
        '[contract_date]': '24-03-2025'
    }

    template_path = 'contract_template.docx'
    output_path = f'dummy_name.docx'

    fill_contract(template_path, output_path, data)
