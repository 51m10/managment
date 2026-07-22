import os
import sys
import flet as ft
import openpyxl
from pypdf import PdfReader

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
            images_col = ft.Column(scroll="always", expand=True)
            try:
                # استفاده از pypdf برای خواندن و استخراج محتوای صفحات به صورت متن یا مدیریت آن
                reader = PdfReader(PDF_FILE)
                start_idx = item['start'] - 1
                end_idx = min(item['end'], len(reader.pages))
                
                for i in range(start_idx, end_idx):
                    page_obj = reader.pages[i]
                    page_text = page_obj.extract_text() or f"صفحه {i + 1}"
                    
                    # نمایش محتوای صفحه به صورت کارت‌های متنی یا ساختار یافته برای جلوگیری از خطای باینری fitz روی اندروید
                    images_col.controls.append(
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Text(f"--- صفحه {i + 1} ---", weight="bold", color=ft.colors.BLUE),
                                    ft.Text(page_text[:500] + ("..." if len(page_text) > 500 else ""))
                                ]),
                                padding=15
                            )
                        )
                    )
            except Exception as ex:
                images_col.controls.append(ft.Text(f"خطا در پردازش فایل PDF: {ex}"))
                
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
        
        # بارگذاری اولیه لیست
        for item in get_data():
            results.controls.append(
                ft.Card(content=ft.ListTile(
                    title=ft.Text(item['name'], weight="bold"),
                    subtitle=ft.Text(f"صفحات {item['start']} تا {item['end']}"),
                    on_click=lambda e, i=item: show_doc_pages(i)
                ))
            )
        
        page.add(search_field, results)
        page.update()

    build_initial_page()

ft.app(target=main)
