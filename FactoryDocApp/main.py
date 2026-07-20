import flet as ft
import openpyxl
import os
import sys
import fitz  # PyMuPDF

# تابعی برای پیدا کردن مسیر فایل‌ها در کنار برنامه
def get_path(filename):
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), filename)
    return os.path.join(os.path.dirname(__file__), filename)

def main(page: ft.Page):
    page.title = "سامانه مدیریت مستندات"
    page.rtl = True
    page.theme_mode = ft.ThemeMode.LIGHT
    
    EXCEL_FILE = get_path("data.xlsx")
    PDF_FILE = get_path("doc.pdf")

    def get_data():
        rows = []
        if os.path.exists(EXCEL_FILE):
            try:
                wb = openpyxl.load_workbook(EXCEL_FILE, data_only=True)
                sheet = wb.worksheets[0]
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    if row[1]:
                        rows.append({
                            "name": str(row[1]), 
                            "start": int(row[2]), 
                            "end": int(row[3])
                        })
            except Exception as e:
                print(f"Error reading Excel: {e}")
        return rows

    def show_doc_pages(item):
        page.clean()
        back_btn = ft.ElevatedButton("بازگشت به فهرست", on_click=lambda e: build_initial_page())
        page.add(back_btn, ft.Text(f"مستندات: {item['name']}", size=20, weight="bold"))
        
        if os.path.exists(PDF_FILE):
            doc = fitz.open(PDF_FILE)
            images_col = ft.Column(scroll="always", expand=True)
            mat = fitz.Matrix(2, 2) 
            
            for i in range(item['start'] - 1, item['end']): 
                pix = doc.load_page(i).get_pixmap(matrix=mat)
                img_path = f"page_{i}.png"
                pix.save(img_path)
                images_col.controls.append(ft.Image(src=img_path, width=800))
            page.add(images_col)
        else:
            page.add(ft.Text("فایل PDF پیدا نشد!"))
        page.update()

    def build_initial_page():
        page.clean()
        results = ft.ListView(expand=True, spacing=10)
        
        def update_list(e):
            search_text = e.control.value.lower()
            results.controls.clear()
            for item in get_data():
                if search_text in item['name'].lower():
                    results.controls.append(
                        ft.Card(content=ft.ListTile(
                            title=ft.Text(item['name'], weight="bold"),
                            subtitle=ft.Text(f"صفحات {item['start']} تا {item['end']}"),
                            on_click=lambda e, i=item: show_doc_pages(i)
                        ))
                    )
            results.update()

        search_field = ft.TextField(label="جستجو در نام دستگاه‌ها...", on_change=update_list)
        page.add(search_field, results)
        page.update()

    build_initial_page()

ft.run(main)