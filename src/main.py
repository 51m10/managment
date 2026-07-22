import flet as ft
import openpyxl
from pypdf import PdfReader
import os

def main(page: ft.Page):
    page.title = "Factory Doc App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # المان نمایش وضعیت و خروجی پردازش
    status_text = ft.Text("آماده برای بارگذاری و پردازش اسناد...", size=14, weight=ft.FontWeight.BOLD)
    
    # فیلد جستجو (در پایین صفحه)
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

    # نوار جستجو در پایین
    bottom_search_bar = ft.Row(
        controls=[search_input, search_button],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # تابع پردازش فایل‌های انتخاب شده (نمونه‌ای برای تست openpyxl و pypdf)
    def process_file_path(file_path):
        try:
            if file_path.endswith('.xlsx'):
                # پردازش فایل اکسل با openpyxl
                wb = openpyxl.load_workbook(file_path, read_only=True)
                sheet_names = wb.sheetnames
                status_text.value = f"فایل اکسل بار شد. شیت‌ها: {', '.join(sheet_names)}"
            elif file_path.endswith('.pdf'):
                # پردازش فایل PDF با pypdf
                reader = PdfReader(file_path)
                num_pages = len(reader.pages)
                status_text.value = f"فایل PDF بار شد. تعداد صفحات: {num_pages}"
            else:
                status_text.value = "فرمت فایل پشتیبانی نمی‌شود."
        except Exception as ex:
            status_text.value = f"خطا در پردازش فایل: {str(ex)}"
        page.update()

    # مدیریت انتخاب فایل (می‌توانید با FilePicker فلت ترکیب کنید)
    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            process_file_path(file_path)

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    upload_button = ft.ElevatedButton(
        text="انتخاب فایل اکسل یا PDF",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda _: file_picker.pick_files(allowed_extensions=["xlsx", "pdf"])
    )

    # چیدمان اصلی صفحه
    page.add(
        ft.Column(
            controls=[
                ft.Text("سیستم مدیریت اسناد کارخانه", size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                upload_button,
                ft.VerticalDivider(height=20),
                status_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        # قرار گرفتن نوار جستجو در پایین صفحه
        bottom_search_bar
    )

ft.app(target=main)
