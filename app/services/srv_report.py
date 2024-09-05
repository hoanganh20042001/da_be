from docx import Document
import os
from datetime import datetime
def generate_docx_from_template(template_path: str, full_name: str, date_birth: str,unit:str,doctor:str,time:str,diseases:str,note:str,result:str) -> str:
    # Mở file template DOCX
    doc = Document(template_path)
    now = datetime.now()
    current_day = now.strftime('%d')
    current_month = now.strftime('%m')
    current_year = now.strftime('%Y')
    # Thay thế các placeholder trong file DOCX
    for paragraph in doc.paragraphs:
        if "{{ full_name }}" in paragraph.text:
            paragraph.text = paragraph.text.replace("{{ full_name }}", full_name)
        if "{{ date_birth }}" in paragraph.text:
            paragraph.text = paragraph.text.replace("{{ date_birth }}", date_birth)
        if "{{ day }}" in paragraph.text:
            paragraph.text = paragraph.text.replace("{{ day }}", current_day)
        if "{{ month }}" in paragraph.text:
            paragraph.text = paragraph.text.replace("{{ month }}", current_month)
        if "{{ unit }}" in paragraph.text:
            paragraph.text = paragraph.text.replace("{{ unit }}", unit)
        if "{{ year }}" in paragraph.text:
            paragraph.text = paragraph.text.replace("{{ year }}", current_year)
        if "{{ doctor }}" in paragraph.text:
            paragraph.text = paragraph.text.replace("{{ doctor }}", doctor)
        if "{{ time }}" in paragraph.text:
            paragraph.text = paragraph.text.replace("{{ time }}", time)
        if "{{ diseases }}" in paragraph.text:
            paragraph.text = paragraph.text.replace("{{ diseases }}", diseases)
        if "{{ note }}" in paragraph.text:
            paragraph.text = paragraph.text.replace("{{ note }}", note)
        if "{{ result }}" in paragraph.text:
            paragraph.text = paragraph.text.replace("{{ result }}", result)
    
    # Đặt tên file mới dựa trên thời gian hiện tại
    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    output_path = os.path.join("files/report", filename)
    
    # Lưu file DOCX vào thư mục 'reports'
    doc.save(output_path)
    
    return output_path
