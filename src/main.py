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

    status_text = ft.Text("لطفاً فایل شرکت را به پوشه اسناد اضافه کنید.", size=13, weight=ft.FontWeight.BOLD)
    
    # دریافت مسیر پوشه اختصاصی اسناد در حافظه داخلی اپلیکیشن (بدون نیاز به دسترسی‌های پیچیده اندروید)
    docs_dir = page.get_app_storage_dir() if hasattr(page, 'get_app_storage_dir') else "."
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir, exist_ok=True)

    # لیست کشویی برای نمایش فایل‌های شرکت‌ها که بعد از نصب اضافه شده‌اند
    company_dropdown = ft.Dropdown(
        label="انتخاب شرکت / فایل اسناد",
        hint_text="فایلی یافت نشد",
        expand=True,
        border_radius=10
    )

    def refresh_file_list():
        # جستجوی فایل‌های اکسل و PDF در پوشه اسناد برنامه
        files = []
        if os.path.exists(docs_dir):
            files = [f for f in os.listdir(docs_dir) if f.endswith(('.xlsx', '.pdf'))]
        
        company_dropdown.options = [ft.dropdown.Option(f) for f in files]
        if files:
            status_text.value = f"تعداد {len(files)} فایل شرکت یافت شد."
        else:
            status_text.value = f"هیچ فایلی در پوشه اسناد نیست. مسیر:\n{docs_dir}"
        page.update()

    def process_selected_company_file(e):
        selected_file = company_dropdown.value
        if not selected_file:
            status_text.value = "لطفاً ابتدا یک شرکت/فایل را انتخاب کنید."
            page.update()
            return

        file_path = os.path.join(docs_dir, selected_file)
        try:
            if file_path.endswith('.xlsx'):
                wb = openpyxl.load_workbook(file_path, read_only=True)
                status_text.value = f"فایل اکسل '{selected_file}' بار شد. شیت‌ها: {', '.join(wb.sheetnames)}"
            elif file_path.endswith('.pdf'):
                reader = PdfReader(file_path)
                status_text.value = f"فایل PDF '{selected_file}' بار شد. تعداد صفحات: {len(reader.pages)}"
        except Exception as ex:
            status_text.value = f"خطا در خواندن فایل شرکت."
        page.update()

    # دکمه‌ای برای به‌روزرسانی لیست فایل‌ها (اگر شرکت جدیدی فایلی ریخت)
    refresh_button = ft.TextButton(
        content=ft.Row([ft.Icon(ft.Icons.REFRESH), ft.Text("بارگذاری مجدد لیست")], spacing=5),
        on_click=lambda _: refresh_file_list()
    )

    select_button = ft.TextButton(
        content=ft.Row([ft.Icon(ft.Icons.CHECK), ft.Text("انتخاب و پردازش فایل شرکت")], spacing=5),
        on_click=process_selected_company_file
    )

    # بخش جستجو برای مهندسان
    search_input = ft.TextField(
        hint_text="جستجو در اسناد شرکت انتخاب شده...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=10,
        expand=True
    )

    def on_search_click(e):
        query = search_input.value
        if query:
            status_text.value = f"در حال جستجوی مهندسی برای: '{query}'"
        else:
            status_text.value = "لطفاً عبارت جستجو را وارد کنید."
        page.update()

    search_button = ft.TextButton(
        content=ft.Row([ft.Icon(ft.Icons.SEARCH), ft.Text("جستجو")], spacing=5),
        on_click=on_search_click
    )

    bottom_search_bar = ft.Row(
        controls=[search_input, search_button],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # بارگذاری اولیه لیست در شروع برنامه
    refresh_file_list()

    page.add(
        ft.Column(
            controls=[
                ft.Container(height=15),
                ft.Text("سیستم مدیریت اسناد کارخانه", size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                company_dropdown,
                ft.Row([refresh_button, select_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
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
