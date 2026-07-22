import flet as ft
import openpyxl
from pypdf import PdfReader
import os

def main(page: ft.Page):
    page.title = "Factory Doc App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    
    # تنظیم جهت صفحه برای زبان فارسی
    page.rtl = True

    status_text = ft.Text("مسیر فایل اکسل یا PDF را در کادر زیر وارد کنید:", size=14, weight=ft.FontWeight.BOLD)
    
    # کادر متنی برای ورود مسیر فایل (بدون استفاده از FilePicker مشکل‌ساز)
    file_path_input = ft.TextField(
        hint_text="مثال: /storage/emulated/0/Download/data.xlsx",
        expand=True,
        border_radius=10
    )

    def process_file_from_path(e):
        file_path = file_path_input.value.strip()
        if not file_path:
            status_text.value = "لطفاً مسیر فایل را وارد کنید."
            page.update()
            return

        status_text.value = f"در حال پردازش فایل: {os.path.basename(file_path)}"
        page.update()
        
        try:
            if file_path.endswith('.xlsx'):
                if not os.path.exists(file_path):
                    status_text.value = "فایل اکسل در مسیر داده شده یافت نشد."
                else:
                    wb = openpyxl.load_workbook(file_path, read_only=True)
                    sheet_names = wb.sheetnames
                    status_text.value = f"فایل اکسل بار شد. شیت‌ها: {', '.join(sheet_names)}"
            elif file_path.endswith('.pdf'):
                if not os.path.exists(file_path):
                    status_text.value = "فایل PDF در مسیر داده شده یافت نشد."
                else:
                    reader = PdfReader(file_path)
                    num_pages = len(reader.pages)
                    status_text.value = f"فایل PDF بار شد. تعداد صفحات: {num_pages}"
            else:
                status_text.value = "فرمت فایل پشتیبانی نمی‌شود (فقط .xlsx یا .pdf)."
        except Exception as ex:
            status_text.value = f"خطا در پردازش فایل: {str(ex)}"
        page.update()

    # استفاده از ElevatedButton استاندارد بدون خطای پارامتر text
    process_button = ft.ElevatedButton(
        text="پردازش فایل",
        icon=ft.Icons.CHECK,
        on_click=process_file_from_path
    )

    search_input = ft.TextField(
        hint_text="جستجو در اسناد...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=10,
        expand=True
    )

    def on_search_click(e):
        query = search_input.value
        if query:
            status_text.value = f"در حال جستجو برای عبارت: '{query}'"
        else:
            status_text.value = "لطفاً متنی را برای جستجو وارد کنید."
        page.update()

    search_button = ft.ElevatedButton(
        text="جستجو",
        icon=ft.Icons.SEARCH,
        on_click=on_search_click
    )

    bottom_search_bar = ft.Row(
        controls=[search_input, search_button],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.add(
        ft.Column(
            controls=[
                ft.Text("سیستم مدیریت اسناد کارخانه", size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("انتخاب فایل:", size=16),
                file_path_input,
                process_button,
                ft.Container(height=20),
                status_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        bottom_search_bar
    )

ft.app(target=main)
