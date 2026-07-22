import flet as ft
import openpyxl
from pypdf import PdfReader
import os

def main(page: ft.Page):
    page.title = "Factory Doc App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.rtl = True

    status_text = ft.Text("مسیر فایل را وارد کنید یا نام فایل را بنویسید:", size=13, weight=ft.FontWeight.BOLD)
    
    file_path_input = ft.TextField(
        hint_text="مثال: data.xlsx یا مسیر کامل",
        expand=True,
        border_radius=10
    )

    def process_file_from_path(e):
        file_path = file_path_input.value.strip()
        if not file_path:
            status_text.value = "لطفاً نام یا مسیر فایل را وارد کنید."
            page.update()
            return

        # اگر کاربر فقط نام فایل را نوشت، در پوشه اسناد داخلی یا پوشه جاری جستجو کنیم
        if not os.path.dirname(file_path):
            # بررسی در مسیرهای رایج یا حافظه داخلی اپ
            potential_paths = [
                file_path,
                os.path.join("/sdcard/Download", file_path),
                os.path.join(page.get_app_storage_dir() if hasattr(page, 'get_app_storage_dir') else "", file_path)
            ]
            found_path = None
            for p in potential_paths:
                if p and os.path.exists(p):
                    found_path = p
                    break
            file_path = found_path if found_path else file_path

        status_text.value = f"در حال پردازش..."
        page.update()
        
        try:
            if not os.path.exists(file_path):
                status_text.value = f"خطا: دسترسی غیرمجاز یا فایل یافت نشد. (Permission/Not Found)"
            elif file_path.endswith('.xlsx'):
                wb = openpyxl.load_workbook(file_path, read_only=True)
                sheet_names = wb.sheetnames
                status_text.value = f"فایل اکسل بار شد. شیت‌ها: {', '.join(sheet_names)}"
            elif file_path.endswith('.pdf'):
                reader = PdfReader(file_path)
                num_pages = len(reader.pages)
                status_text.value = f"فایل PDF بار شد. تعداد صفحات: {num_pages}"
            else:
                status_text.value = "فرمت فایل پشتیبانی نمی‌شود (فقط .xlsx یا .pdf)."
        except Exception as ex:
            status_text.value = f"خطا در دسترسی به فایل (مجوز اندروید محدود است)"
        page.update()

    process_button = ft.TextButton(
        content=ft.Row([ft.Icon(ft.Icons.CHECK), ft.Text("پردازش فایل")], spacing=5),
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

    search_button = ft.TextButton(
        content=ft.Row([ft.Icon(ft.Icons.SEARCH), ft.Text("جستجو")], spacing=5),
        on_click=on_search_click
    )

    bottom_search_bar = ft.Row(
        controls=[search_input, search_button],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.add(
        ft.Column(
            controls=[
                # فاصله ایجاد شده از بالای صفحه برای جلوگیری از چسبیدن متن
                ft.Container(height=15),
                ft.Text("سیستم مدیریت اسناد کارخانه", size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("انتخاب فایل:", size=16),
                file_path_input,
                process_button,
                ft.Container(height=10),
                status_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        bottom_search_bar
    )

ft.app(target=main)
