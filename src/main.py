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

    # تعیین یک مسیر عمومی و در دسترس در حافظه داخلی (پوشه Download)
    # اگر دسترسی محدود باشد، از پوشه داخلی خود اپ استفاده می‌کند
    docs_dir = "/storage/emulated/0/Download/FactoryDocs"
    try:
        if not os.path.exists(docs_dir):
            os.makedirs(docs_dir, exist_ok=True)
    except Exception:
        docs_dir = page.get_app_storage_dir() if hasattr(page, 'get_app_storage_dir') else "."
        if not os.path.exists(docs_dir):
            os.makedirs(docs_dir, exist_ok=True)

    status_text = ft.Text(f"پوشه اسناد:\n{docs_dir}\nلطفاً فایل‌ها را اینجا قرار دهید.", size=12, weight=ft.FontWeight.BOLD)
    
    company_dropdown = ft.Dropdown(
        label="انتخاب شرکت / فایل اسناد",
        hint_text="فایلی یافت نشد",
        expand=True,
        border_radius=10
    )

    def refresh_file_list(e=None):
        files = []
        try:
            if os.path.exists(docs_dir):
                files = [f for f in os.listdir(docs_dir) if f.endswith(('.xlsx', '.pdf'))]
        except Exception:
            files = []
        
        company_dropdown.options = [ft.dropdown.Option(f) for f in files]
        if files:
            status_text.value = f"تعداد {len(files)} فایل پیدا شد. مسیر:\n{docs_dir}"
        else:
            status_text.value = f"فایلی در این مسیر نیست:\n{docs_dir}"
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
        except Exception:
            status_text.value = "خطا در خواندن فایل شرکت."
        page.update()

    refresh_button = ft.TextButton(
        content=ft.Row([ft.Icon(ft.Icons.REFRESH), ft.Text("بارگذاری مجدد")], spacing=5),
        on_click=refresh_file_list
    )

    select_button = ft.TextButton(
        content=ft.Row([ft.Icon(ft.Icons.CHECK), ft.Text("پردازش فایل")], spacing=5),
        on_click=process_selected_company_file
    )

    search_input = ft.TextField(
        hint_text="جستجو در اسناد شرکت...",
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

    refresh_file_list()

    page.add(
        ft.Column(
            controls=[
                ft.Container(height=10),
                ft.Text("سیستم مدیریت اسناد کارخانه", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                company_dropdown,
                ft.Row([refresh_button, select_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=5),
                status_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        bottom_search_bar
    )

ft.app(target=main)
