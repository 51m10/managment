import os
import flet as ft
import openpyxl
from pypdf import PdfReader

def main(page: ft.Page):
    page.title = "سامانه مدیریت مستندات"
    page.rtl = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    app_state = {
        "excel_path": None,
        "excel_name": "فایل اکسل انتخاب نشده است",
        "pdf_path": None,
        "pdf_name": "فایل PDF انتخاب نشده است"
    }

    excel_text = ft.Text(app_state["excel_name"], size=12, color=ft.Colors.RED)
    pdf_text = ft.Text(app_state["pdf_name"], size=12, color=ft.Colors.RED)

    def on_excel_result(e: ft.FilePickerResultEvent):
        if e.files:
            app_state["excel_path"] = e.files[0].path
            app_state["excel_name"] = e.files[0].name
            excel_text.value = f"اکسل: {app_state['excel_name']}"
            excel_text.color = ft.Colors.GREEN
            build_initial_page()

    def on_pdf_result(e: ft.FilePickerResultEvent):
        if e.files:
            app_state["pdf_path"] = e.files[0].path
            app_state["pdf_name"] = e.files[0].name
            pdf_text.value = f"پی‌دی‌اف: {app_state['pdf_name']}"
            pdf_text.color = ft.Colors.GREEN
            build_initial_page()

    excel_picker = ft.FilePicker()
    excel_picker.on_result = on_excel_result

    pdf_picker = ft.FilePicker()
    pdf_picker.on_result = on_pdf_result
    
    page.overlay.extend([excel_picker, pdf_picker])

    def get_data():
        rows = []
        if app_state["excel_path"] and os.path.exists(app_state["excel_path"]):
            try:
                wb = openpyxl.load_workbook(app_state["excel_path"], data_only=True)
                sheet = wb.worksheets[0]
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    if row[1]:
                        rows.append({
                            "name": str(row[1]), 
                            "start": int(row[2]), 
                            "end": int(row[3])
                        })
            except Exception as ex:
                print(f"Error reading Excel: {ex}")
        return rows

    def show_doc_pages(item):
        page.clean()
        back_btn = ft.Button("بازگشت به فهرست", on_click=lambda e: build_initial_page())
        
        page.add(
            ft.Container(height=10),
            back_btn, 
            ft.Container(height=10),
            ft.Text(f"مستندات: {item['name']}", size=20, weight="bold")
.        )
        
        if app_state["pdf_path"] and os.path.exists(app_state["pdf_path"]):
            images_col = ft.Column(scroll="always", expand=True)
            try:
                reader = PdfReader(app_state["pdf_path"])
                start_idx = item['start'] - 1
                end_idx = min(item['end'], len(reader.pages))
                
                for i in range(start_idx, end_idx):
                    page_obj = reader.pages[i]
                    page_text = page_obj.extract_text() or f"صفحه {i + 1}"
                    
                    images_col.controls.append(
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Text(f"--- صفحه {i + 1} ---", weight="bold", color=ft.Colors.BLUE),
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
            page.add(ft.Text("فایل PDF شرکت انتخاب نشده است!"))
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

        search_field = ft.TextField(
            label="جستجو در نام دستگاه‌ها...", 
            on_change=update_list,
            prefix_icon=ft.Icons.SEARCH
        )

        async def pick_excel_click(e):
            await excel_picker.pick_files_async(allowed_extensions=["xlsx"])

        async def pick_pdf_click(e):
            await pdf_picker.pick_files_async(allowed_extensions=["pdf"])

        pick_excel_btn = ft.Button(
            "انتخاب فایل اکسل شرکت", 
            icon=ft.Icons.UPLOAD_FILE,
            on_click=pick_excel_click
        )
        
        pick_pdf_btn = ft.Button(
            "انتخاب فایل PDF شرکت", 
            icon=ft.Icons.PICTURE_AS_PDF,
            on_click=pick_pdf_click
        )

        for item in get_data():
            results.controls.append(
                ft.Card(content=ft.ListTile(
                    title=ft.Text(item['name'], weight="bold"),
                    subtitle=ft.Text(f"صفحات {item['start']} تا {item['end']}"),
                    on_click=lambda e, i=item: show_doc_pages(i)
                ))
            )
        
        page.add(
            ft.Container(height=10),
            ft.Row([pick_excel_btn, excel_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([pick_pdf_btn, pdf_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            search_field,
            ft.Container(height=10),
            results
        )
        page.update()

    build_initial_page()

ft.run(main)
