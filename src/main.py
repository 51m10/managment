import flet as ft
import openpyxl
from pypdf import PdfReader
import os

def main(page: ft.Page):
    page.title = "Factory Doc App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    status_text = ft.Text("آماده برای بارگذاری و پردازش اسناد...", size=14, weight=ft.FontWeight.BOLD)
    
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

    # استفاده از ساختار امن TextButton با محتوا
    search_button = ft.TextButton(
        content=ft.Row([ft.Icon(ft.Icons.SEARCH), ft.Text("جستجو")], spacing=5),
        on_click=on_search_click
    )

    bottom_search_bar = ft.Row(
        controls=[search_input, search_button],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    def process_file_path(file_path):
        try:
            if file_path.endswith('.xlsx'):
                wb = openpyxl.load_workbook(file_path, read_only=True)
                sheet_names = wb.sheetnames
                status_text.value = f"فایل اکسل بار شد. شیت‌ها: {', '.join(sheet_names)}"
            elif file_path.endswith('.pdf'):
                reader = PdfReader(file_path)
                num_pages = len(reader.pages)
                status_text.value = f"فایل PDF بار شد. تعداد صفحات: {num_pages}"
            else:
                status_text.value = "فرمت فایل پشتیبانی نمی‌شود."
        except Exception as ex:
            status_text.value = f"خطا در پردازش فایل: {str(ex)}"
        page.update()

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            process_file_path(file_path)

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    upload_button = ft.TextButton(
        content=ft.Row([ft.Icon(ft.Icons.UPLOAD_FILE), ft.Text("انتخاب فایل اکسل یا PDF")], spacing=5),
        on_click=lambda _: file_picker.pick_files(allowed_extensions=["xlsx", "pdf"])
    )

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
        bottom_search_bar
    )

ft.app(target=main)
