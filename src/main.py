import flet as ft
import openpyxl
from pypdf import PdfReader
import shutil
import os

def main(page: ft.Page):
    page.title = "Factory Doc App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.rtl = True

    # ایجاد پوشه امن داخلی برای ذخیره فایل انتخاب شده
    docs_dir = page.get_app_storage_dir() if hasattr(page, 'get_app_storage_dir') else "."
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir, exist_ok=True)

    status_text = ft.Text("لطفاً با دکمه زیر فایل شرکت را انتخاب کنید.", size=12, weight=ft.FontWeight.BOLD)
    
    company_dropdown = ft.Dropdown(
        label="انتخاب فایل اسناد",
        hint_text="فایلی انتخاب نشده است",
        expand=True,
        border_radius=10
    )

    def update_dropdown():
        files = []
        if os.path.exists(docs_dir):
            files = [f for f in os.listdir(docs_dir) if f.endswith(('.xlsx', '.pdf'))]
        company_dropdown.options = [ft.dropdown.Option(f) for f in files]
        if files:
            status_text.value = f"تعداد {len(files)} فایل آماده است."
        else:
            status_text.value = "فایلی انتخاب نشده است."
        page.update()

    # تعریف فایل‌پیکر و اضافه کردن به overlay صفحه (بخش حیاتی برای اندروید)
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    def on_dialog_result(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            selected_file = e.files[0]
            source_path = selected_file.path
            file_name = selected_file.name
            
            dest_path = os.path.join(docs_dir, file_name)
            try:
                # کپی کردن فایل انتخاب شده به پوشه داخلی اپ
                if source_path != dest_path:
                    shutil.copy(source_path, dest_path)
                
                update_dropdown()
                company_dropdown.value = file_name
                status_text.value = f"فایل '{file_name}' با موفقیت اضافه شد."
            except Exception as ex:
                status_text.value = "خطا در بارگذاری فایل انتخاب شده."
            page.update()

    file_picker.on_result = on_dialog_result

    def process_file(e):
        selected_file = company_dropdown.value
        if not selected_file:
            status_text.value = "لطفاً ابتدا یک فایل را انتخاب کنید."
            page.update()
            return

        file_path = os.path.join(docs_dir, selected_file)
        try:
            if file_path.endswith('.xlsx'):
                wb = openpyxl.load_workbook(file_path, read_only=True)
                status_text.value = f"فایل اکسل بار شد. شیت‌ها: {', '.join(wb.sheetnames)}"
            elif file_path.endswith('.pdf'):
                reader = PdfReader(file_path)
                status_text.value = f"فایل PDF بار شد. تعداد صفحات: {len(reader.pages)}"
        except Exception:
            status_text.value = "خطا در خواندن محتوای فایل."
        page.update()

    # دکمه فراخوانی فایل‌پیکر با فیلتر روی فایل‌های اکسل و PDF
    pick_button = ft.TextButton(
        content=ft.Row([ft.Icon(ft.Icons.FOLDER_OPEN), ft.Text("انتخاب فایل از گوشی")], spacing=5),
        on_click=lambda _: file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["xlsx", "pdf"]
        )
    )

    process_button = ft.TextButton(
        content=ft.Row([ft.Icon(ft.Icons.CHECK), ft.Text("پردازش فایل")], spacing=5),
        on_click=process_file
    )

    search_input = ft.TextField(
        hint_text="جستجو در اسناد...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=10,
        expand=True
    )

    def on_search(e):
        q = search_input.value
        status_text.value = f"جستجو برای: '{q}'" if q else "عبارت جستجو خالی است."
        page.update()

    search_btn = ft.TextButton(
        content=ft.Row([ft.Icon(ft.Icons.SEARCH), ft.Text("جستجو")], spacing=5),
        on_click=on_search
    )

    update_dropdown()

    page.add(
        ft.Column(
            controls=[
                ft.Container(height=10),
                ft.Text("سیستم مدیریت اسناد کارخانه", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                company_dropdown,
                ft.Row([pick_button, process_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=5),
                status_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        ft.Row([search_input, search_btn])
    )

ft.app(target=main)
