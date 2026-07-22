import flet as ft

def main(page: ft.Page):
    page.title = "Factory Doc App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # المان‌های نمایش خروجی یا وضعیت
    status_text = ft.Text("آماده برای پردازش اسناد...", size=16, weight=ft.FontWeight.BOLD)
    
    # فیلد جستجو (نوار جستجو در پایین قرار می‌گیرد)
    search_input = ft.TextField(
        hint_text="متن مورد نظر را جستجو کنید...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=10,
        expand=True
    )

    def on_search_click(e):
        query = search_input.value
        if query:
            status_text.value = f"در حال جستجو برای: '{query}'"
        else:
            status_text.value = "لطفاً عبارتی را برای جستجو وارد کنید."
        page.update()

    search_button = ft.ElevatedButton(
        text="جستجو",
        icon=ft.Icons.SEARCH,
        on_click=on_search_click
    )

    # بخش پایینی شامل نوار جستجو و دکمه آن
    bottom_search_bar = ft.Row(
        controls=[search_input, search_button],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # دکمه‌های اصلی اپلیکیشن
    def pick_file(e):
        status_text.value = "فایل با موفقیت انتخاب شد و در حال پردازش است."
        page.update()

    upload_button = ft.ElevatedButton(
        text="انتخاب فایل اکسل یا PDF",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=pick_file
    )

    # چیدمان اصلی صفحه
    page.add(
        ft.Column(
            controls=[
                ft.Text("سیستم مدیریت اسناد کارخانه", size=22, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                upload_button,
                ft.VerticalDivider(height=20),
                status_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        ),
        # قرار دادن نوار جستجو در بخش پایینی صفحه
        bottom_search_bar
    )

ft.app(target=main)
