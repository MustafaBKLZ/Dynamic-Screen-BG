import flet as ft
import os
import sys
import threading
import time
from wallpaper_service import service

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class NumberStepper(ft.Row):
    def __init__(self, value=10, min_value=1, step=1, on_change=None):
        super().__init__()
        self.value = value
        self.min_value = min_value
        self.step = step
        self.on_change = on_change
        
        self.text_field = ft.TextField(
            value=str(value), 
            text_size=12, 
            width=50, 
            height=30, 
            content_padding=5,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_submit=self._on_submit,
            border_radius=5,
            border_color=ft.Colors.GREY_700,
            bgcolor=ft.Colors.GREY_900
        )
        
        self.btn_minus = ft.IconButton(
            icon=ft.Icons.REMOVE, 
            icon_size=14, 
            width=30, 
            height=30, 
            on_click=self.decrement,
            style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_800, shape=ft.RoundedRectangleBorder(radius=5))
        )
        
        self.btn_plus = ft.IconButton(
            icon=ft.Icons.ADD, 
            icon_size=14, 
            width=30, 
            height=30, 
            on_click=self.increment,
            style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_800, shape=ft.RoundedRectangleBorder(radius=5))
        )
        
        self.controls = [self.btn_minus, self.text_field, self.btn_plus]
        self.spacing = 5
        self.alignment = ft.MainAxisAlignment.CENTER

    def increment(self, e):
        self.value += self.step
        self.text_field.value = str(self.value)
        if self.text_field.page:
             self.text_field.update()
        if self.on_change: self.on_change(e)

    def decrement(self, e):
        if self.value > self.min_value:
            self.value -= self.step
            self.text_field.value = str(self.value)
            if self.text_field.page:
                 self.text_field.update()
            if self.on_change: self.on_change(e)

    def _on_submit(self, e):
        try:
            val = int(e.control.value)
            self.value = max(self.min_value, val)
        except ValueError:
            pass
        self.text_field.value = str(self.value)
        if self.text_field.page:
             self.text_field.update()
        if self.on_change: self.on_change(e)
        
    def get_value(self):
        return int(self.text_field.value)
        
    def set_value(self, val):
        self.value = int(val)
        self.text_field.value = str(val)
        if self.text_field.page:
             self.text_field.update()

class MonitorCard(ft.Container):
    def __init__(self, monitor_data, app):
        super().__init__()
        self.monitor_data = monitor_data
        self.monitor_name = monitor_data['name']
        self.app = app
        self.is_selected = False
        
        self.padding = 10
        self.border_radius = 8
        self.ink = True
        self.on_click = self.select_monitor
        self.animate = ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        
        display_name = self.monitor_name.replace(r"\\.\DISPLAY", "Display ")
        
        self.text_name = ft.Text(
            display_name, 
            size=14, 
            weight=ft.FontWeight.W_600,
            color=ft.Colors.WHITE
        )
        self.text_res = ft.Text(
            f"{monitor_data['width']}x{monitor_data['height']}", 
            size=11, 
            color=ft.Colors.GREY_500
        )
        self.status_indicator = ft.Container(
            width=8, height=8, border_radius=4, bgcolor=ft.Colors.GREY_800
        )
        
        self.content = ft.Row([
            ft.Icon(ft.Icons.DESKTOP_WINDOWS_ROUNDED, color=ft.Colors.BLUE_GREY_200, size=20),
            ft.Column([self.text_name, self.text_res], spacing=0, expand=True),
            self.status_indicator
        ], alignment=ft.MainAxisAlignment.START, spacing=15)

    def select_monitor(self, e):
        self.app.select_monitor(self.monitor_name)

    def set_selected(self, selected):
        self.is_selected = selected
        self.bgcolor = ft.Colors.BLUE_GREY_900 if selected else None
        self.border = ft.border.all(1, ft.Colors.BLUE_500) if selected else None
        if self.page:
            self.update()
        
    def set_active(self, active):
        self.status_indicator.bgcolor = ft.Colors.GREEN_400 if active else ft.Colors.GREY_800
        if self.page:
            self.status_indicator.update()

import json

class LanguageManager:
    def __init__(self):
        self.current_lang = "tr"
        self.translations = {}
        self.load_locales()

    def load_locales(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            locales_dir = os.path.join(base_path, "locales")
            
            with open(os.path.join(locales_dir, "tr.json"), "r", encoding="utf-8") as f:
                self.translations["tr"] = json.load(f)
            with open(os.path.join(locales_dir, "en.json"), "r", encoding="utf-8") as f:
                self.translations["en"] = json.load(f)
        except Exception as e:
            print(f"Error loading locales: {e}")
            self.translations["tr"] = {}
            self.translations["en"] = {}

    def t(self, key, **kwargs):
        text = self.translations.get(self.current_lang, {}).get(key, key)
        if kwargs:
            try:
                text = text.format(**kwargs)
            except:
                pass
        return text

    def set_lang(self, lang):
        if lang in ["tr", "en"]:
            self.current_lang = lang

class App(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self.page = page
        self.lm = LanguageManager()
        
        # Load saved app settings
        app_settings = service.get_app_settings()
        saved_lang = app_settings.get('language', 'tr')
        self.show_logs = app_settings.get('show_logs', True)
        
        # Set language
        self.lm.set_lang(saved_lang)
        
        self.page.title = self.lm.t("app_title")
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#1a1c21"
        self.page.padding = 0
        
        self.selected_monitor = None
        self.monitor_cards = {}
        
        # UI Components
        self.setup_ui()
        
        # Load Monitors
        self.load_monitors()
        
        # Background Timer Thread
        self.stop_event = threading.Event()
        self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
        self.timer_thread.start()

    def setup_ui(self):
        self.controls.clear()

        # Sidebar content
        self.sidebar_content = ft.Column(spacing=5, scroll=ft.ScrollMode.AUTO, expand=True) 
        self.log_list = ft.ListView(expand=True, spacing=2, padding=10, auto_scroll=True)
        
        self.log_container_wrapper = ft.Column([
                ft.Divider(color="#2c3038", height=10, thickness=1),
                ft.Row([
                    ft.Text(self.lm.t("log_history"), size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_400),
                    ft.Icon(ft.Icons.HISTORY, size=14, color=ft.Colors.BLUE_GREY_400)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(
                    content=self.log_list,
                    height=200, 
                    bgcolor="#181a1f",
                    border_radius=8,
                    padding=5
                )
            ], spacing=5)
        self.log_container_wrapper.visible = self.show_logs

        self.sidebar = ft.Container(
            width=320,
            bgcolor="#20232a",
            padding=20,
            border=ft.border.only(right=ft.BorderSide(1, "#2c3038")),
            content=ft.Column([
                ft.Text(self.lm.t("monitors"), size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_400),
                ft.Container(height=5),
                self.sidebar_content,
                # Removed explicit spacer to allow sidebar_content to take all space
                self.log_container_wrapper,
                ft.Container(height=5),
                 ft.ElevatedButton(
                    self.lm.t("settings"),
                    icon=ft.Icons.SETTINGS,
                    bgcolor=ft.Colors.GREY_800,
                    color=ft.Colors.WHITE,
                    width=280,
                    on_click=self.open_settings,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=15
                    )
                ),
                ft.Column([
                    ft.Container(
                        content=ft.Text(
                            self.lm.t("created_by"), 
                            size=9, 
                            color=ft.Colors.GREY_700,
                            text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.W_500
                        ),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(bottom=2)
                    ),
                    ft.Container(
                        content=ft.Row([
                            ft.IconButton(
                                content=ft.Image(
                                    src=resource_path("github.svg"),
                                    width=16,
                                    height=16,
                                    color=ft.Colors.GREY_600
                                ),
                                tooltip="GitHub",
                                url="https://github.com/MustafaBKLZ",
                                style=ft.ButtonStyle(
                                    padding=2,
                                )
                            ),
                            ft.IconButton(
                                content=ft.Image(
                                    src=resource_path("x.svg"),
                                    width=16,
                                    height=16,
                                    color=ft.Colors.GREY_600
                                ),
                                tooltip="X (Twitter)",
                                url="https://x.com/BukulmezMustafa",
                                style=ft.ButtonStyle(
                                    padding=2,
                                )
                            ),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=0),
                        alignment=ft.alignment.center,
                    )
                ], spacing=0)
            ])
        )
        
        # Header Components
        self.header_title = ft.Text(self.lm.t("no_monitor_selected"), size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        self.header_subtitle = ft.Text(self.lm.t("select_monitor_msg"), size=12, color=ft.Colors.GREY_500)
        
        self.switch_enabled = ft.Switch(
            label=self.lm.t("auto_change"), 
            value=False, 
            disabled=True, 
            scale=0.8,
            label_position=ft.LabelPosition.LEFT,
            on_change=self.save_settings
        )
        
        self.input_interval = NumberStepper(value=60, on_change=None)

        # Action Buttons
        self.btn_save = ft.ElevatedButton(
            self.lm.t("save"), 
            icon=ft.Icons.SAVE_ROUNDED, 
            on_click=self.save_settings, 
            bgcolor=ft.Colors.BLUE_600, 
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                padding=15,
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )

        self.btn_add_images = ft.ElevatedButton(
            self.lm.t("add_images"), 
            icon=ft.Icons.ADD_PHOTO_ALTERNATE_ROUNDED, 
            on_click=lambda _: self.file_picker.pick_files(allow_multiple=True, file_type=ft.FilePickerFileType.IMAGE),
            bgcolor=ft.Colors.INDIGO_500,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                padding=15,
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )
        
        self.btn_clear_all = ft.TextButton(
            self.lm.t("clear_all"), 
            icon=ft.Icons.DELETE_SWEEP_OUTLINED, 
            icon_color=ft.Colors.RED_400, 
            style=ft.ButtonStyle(color=ft.Colors.RED_400),
            on_click=self.clear_all_images,
        )

        # Monitor Settings Panel
        self.monitor_settings_panel = ft.Container(
            visible=False, 
            padding=20,
            bgcolor="#252830",
            border_radius=12,
            content=ft.Row([
                ft.Column([self.header_title, self.header_subtitle], spacing=2),
                ft.Container(expand=True),
                ft.Row([
                    self.switch_enabled,
                    ft.Container(width=10),
                    self.input_interval,
                    ft.Container(width=10),
                    self.btn_save
                ], alignment=ft.MainAxisAlignment.END, spacing=10)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )
        
        # Images Grid
        self.images_grid = ft.GridView(
            runs_count=5,
            max_extent=160,
            child_aspect_ratio=1.6,
            spacing=15,
            run_spacing=15,
            padding=20,
            expand=True
        )

        self.main_content = ft.Container(
            expand=True,
            padding=20,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#1a1c21", "#131519"]
            ),
            content=ft.Column([
                self.monitor_settings_panel,
                ft.Container(height=10),
                ft.Row([
                    ft.Container(expand=True), 
                    self.btn_add_images
                ], alignment=ft.MainAxisAlignment.END),
                ft.Container(height=10),
                ft.Container(
                    content=ft.Column([
                        self.images_grid,
                        ft.Container(
                            content=self.btn_clear_all,
                            alignment=ft.alignment.bottom_right,
                            padding=ft.padding.only(top=10, right=10)
                        )
                    ]),
                    expand=True
                )
            ])
        )

        self.file_picker = ft.FilePicker(on_result=self.on_file_pick)
        self.page.overlay.append(self.file_picker)

        # Build Layout
        self.controls = [
            ft.Row([self.sidebar, ft.VerticalDivider(width=1, color="#2c3038"), self.main_content], expand=True, spacing=0)
        ]
        
        # Connect Logger
        service.set_log_callback(self.update_log)
        
    def open_settings(self, e):
        print("Settings button clicked!")
        
        def change_lang(e):
            print(f"Language changed to: {e.control.value}")
            new_lang = e.control.value
            self.lm.set_lang(new_lang)
            # Save to config
            service.update_app_settings('language', new_lang)
            # Close settings
            self.settings_overlay.visible = False
            self.settings_overlay.update()
            # Rebuild UI
            self.setup_ui() 
            self.load_monitors()
            self.update() 
            self.page.update()

        def toggle_logs(e):
            print(f"Logs toggled: {e.control.value}")
            self.show_logs = e.control.value
            # Save to config
            service.update_app_settings('show_logs', self.show_logs)
            self.log_container_wrapper.visible = self.show_logs
            self.update()
            self.page.update()

        def close_settings(e):
            print("Closing settings")
            self.settings_overlay.visible = False
            self.settings_overlay.update()

        lang_dropdown = ft.Dropdown(
            label=self.lm.t("language"),
            value=self.lm.current_lang,
            options=[
                ft.dropdown.Option("tr", "Türkçe"),
                ft.dropdown.Option("en", "English"),
            ],
            on_change=change_lang,
            width=250
        )

        log_switch = ft.Switch(
            label=self.lm.t("show_logs"),
            value=self.show_logs,
            on_change=toggle_logs
        )

        # Create overlay with settings panel
        settings_panel = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(self.lm.t("settings"), size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.IconButton(ft.Icons.CLOSE, on_click=close_settings, icon_color=ft.Colors.WHITE)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(color=ft.Colors.GREY_700),
                ft.Container(height=10),
                lang_dropdown,
                ft.Container(height=20),
                log_switch,
                ft.Container(height=20),
                ft.ElevatedButton(
                    "OK",
                    on_click=close_settings,
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE,
                    width=100
                )
            ], tight=True, spacing=10),
            bgcolor="#2a2d35",
            border_radius=12,
            padding=30,
            width=400,
            shadow=ft.BoxShadow(
                spread_radius=5,
                blur_radius=15,
                color=ft.Colors.BLACK54
            )
        )

        self.settings_overlay = ft.Container(
            content=ft.Stack([
                ft.Container(  # Semi-transparent background
                    bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                    expand=True,
                    on_click=close_settings
                ),
                ft.Container(  # Center the panel
                    content=settings_panel,
                    alignment=ft.alignment.center,
                    expand=True
                )
            ]),
            visible=True,
            expand=True
        )
        
        # Add overlay to page
        self.page.overlay.append(self.settings_overlay)
        self.page.update()
        print("Settings overlay added and visible")

    def update_log(self, message):
        if not self.show_logs: return
        timestamp = time.strftime("%H:%M")
        self.log_list.controls.insert(0, ft.Text(f"[{timestamp}] {message}", size=11, font_family="Consolas", color=ft.Colors.BLUE_GREY_200))
        if len(self.log_list.controls) > 50:
            self.log_list.controls.pop()
        try:
            if self.page:
                self.log_list.update()
        except:
            pass

    def load_monitors(self):
        service.detect_monitors()
        self.sidebar_content.controls.clear()
        self.monitor_cards = {}
        
        for m in service.monitors:
            card = MonitorCard(m, self)
            self.monitor_cards[m['name']] = card
            self.sidebar_content.controls.append(card)
            
            # Set init active status
            config = service.get_config(m['name'])
            card.set_active(config.get('enabled', False))
            
        if service.monitors:
            self.select_monitor(service.monitors[0]['name'])

    def select_monitor(self, name):
        # Deselect old
        if self.selected_monitor:
            old_card = self.monitor_cards.get(self.selected_monitor)
            if old_card: old_card.set_selected(False)
            
        self.selected_monitor = name
        new_card = self.monitor_cards.get(name)
        if new_card: new_card.set_selected(True)
        
        # Update Content
        config = service.get_config(name)
        self.header_title.value = name.replace(r"\\.\DISPLAY", "Display ")
        
        self.monitor_settings_panel.visible = True
        if self.monitor_settings_panel.page:
             self.monitor_settings_panel.update()
        
        self.switch_enabled.disabled = False
        self.switch_enabled.value = config.get('enabled', False)
        
        self.input_interval.set_value(config.get('interval', 60))
        
        self.load_images(config.get('images', []))
        if self.page:
             self.page.update()

    def load_images(self, images):
        self.images_grid.controls.clear()
        
        for i, img_path in enumerate(images):
            # Overlay Buttons (More Subtle)
            delete_btn = ft.Container(
                content=ft.Icon(ft.Icons.CLOSE_ROUNDED, size=16, color=ft.Colors.WHITE70),
                width=24, height=24,
                bgcolor=ft.Colors.BLACK54,
                border_radius=12,
                alignment=ft.alignment.center,
                on_click=lambda e, p=img_path: self.remove_image(p),
                tooltip="Kaldır"
            )
            
            # Draggable Image Card
            img_card = ft.Container(
                content=ft.Stack([
                    ft.Image(
                        src=img_path, 
                        fit=ft.ImageFit.COVER, 
                        border_radius=8, 
                        opacity=1.0,
                        width=160, # Explicit width to fill container
                        height=100 # Explicit height to fill container
                    ),
                    ft.Container(
                        content=delete_btn,
                        right=5,
                        top=5,
                        visible=False,
                    )
                ]),
                bgcolor="#20232a",
                border_radius=8,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=5,
                    color=ft.Colors.BLACK54,
                    offset=ft.Offset(0, 2),
                ),
                width=160,
                height=100
            )
            
            # Make delete button always visible but cleaner
            img_card.content.controls[1].visible = True 

            draggable = ft.Draggable(
                group="images",
                content=img_card,
                content_feedback=ft.Container(
                    width=120, height=80, 
                    content=ft.Image(src=img_path, fit=ft.ImageFit.COVER, opacity=0.8, border_radius=8),
                ),
                data=i 
            )

            drag_target = ft.DragTarget(
                group="images",
                content=draggable,
                on_accept=lambda e, idx=i: self.on_drag_accept(e, idx)
            )
            
            self.images_grid.controls.append(drag_target)

        if self.images_grid.page:
             self.images_grid.update()
        
    def on_drag_accept(self, e: ft.DragTargetEvent, dest_index):
        try:
             src_index = self.page.get_control(e.src_id).data
             if src_index != dest_index:
                 self.shift_image(src_index, dest_index)
        except Exception:
            pass

    def shift_image(self, src_index, dest_index):
        if self.selected_monitor:
            service.shift_image(self.selected_monitor, src_index, dest_index)
            config = service.get_config(self.selected_monitor)
            self.load_images(config.get('images', []))
            
    def save_settings(self, e):
         if self.selected_monitor:
            val = self.input_interval.get_value()
            is_enabled = self.switch_enabled.value
            
            service.update_config(self.selected_monitor, 'interval', val)
            service.update_config(self.selected_monitor, 'enabled', is_enabled)
            
            # Update Active Status in Sidebar
            if self.monitor_cards.get(self.selected_monitor):
                self.monitor_cards[self.selected_monitor].set_active(is_enabled)

            self.page.snack_bar = ft.SnackBar(
                content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_400), ft.Text("Ayarlar Kaydedildi")], alignment=ft.MainAxisAlignment.START),
                bgcolor="#252830"
            )
            self.page.snack_bar.open = True
            self.page.update()

    def on_file_pick(self, e: ft.FilePickerResultEvent):
        if e.files and self.selected_monitor:
            new_images = [f.path for f in e.files]
            config = service.get_config(self.selected_monitor)
            current_images = config.get('images', [])
            
            updated_images = current_images + new_images
            service.update_config(self.selected_monitor, 'images', updated_images)
            self.load_images(updated_images)
            self.page.snack_bar = ft.SnackBar(ft.Text(f"{len(new_images)} resim eklendi"), bgcolor=ft.Colors.GREEN_900)
            self.page.snack_bar.open = True
            self.page.update()

    def remove_image(self, path):
         if self.selected_monitor:
            config = service.get_config(self.selected_monitor)
            current_images = config.get('images', [])
            if path in current_images:
                current_images.remove(path)
                service.update_config(self.selected_monitor, 'images', current_images)
                self.load_images(current_images)

    def clear_all_images(self, e):
        if self.selected_monitor:
             service.update_config(self.selected_monitor, 'images', [])
             self.load_images([])
             self.page.snack_bar = ft.SnackBar(ft.Text("Galeri temizlendi"), bgcolor=ft.Colors.RED_900)
             self.page.snack_bar.open = True
             self.page.update()

    def run_timer(self):
        """Background thread to check timers for each monitor and update wallpaper."""
        last_checks = {} 
        current_wallpapers = {} 
        
        # Load init state
        for m in service.monitors:
            last_checks[m['name']] = 0
            cfg = service.get_config(m['name'])
            if cfg.get('images'):
                current_wallpapers[m['name']] = cfg['images'][0]

        while not self.stop_event.is_set():
            now = time.time()
            needs_update = False
            
            for m in service.monitors:
                name = m['name']
                cfg = service.get_config(name)
                
                if cfg.get('enabled') and cfg.get('images'):
                    interval = cfg.get('interval', 60)
                    if now - last_checks.get(name, 0) >= interval:
                        last_checks[name] = now
                        images = cfg['images']
                        idx = cfg.get('last_index', 0)
                        idx = (idx + 1) % len(images)
                        service.update_config(name, 'last_index', idx)
                        current_wallpapers[name] = images[idx]
                        needs_update = True
                
                if cfg.get('enabled') and cfg.get('images') and name not in current_wallpapers:
                     current_wallpapers[name] = cfg['images'][0]
                     needs_update = True

            if needs_update:
                final_path = service.generate_stitched_wallpaper(current_wallpapers)
                if final_path:
                    service.set_system_wallpaper(final_path)
            
            time.sleep(1)


import pystray
from PIL import Image as PilImage

def main(page: ft.Page):
    app = App(page)
    page.add(app)
    
    # System Tray Setup
    def on_tray_open(icon, item):
        page.window.visible = True
        page.window.minimized = False
        page.window.prevent_close = True
        page.update()

    def on_tray_exit(icon, item):
        icon.stop()
        page.window.destroy()
        os._exit(0)

    def run_tray():
        try:
            # Default icon
            image = PilImage.new('RGB', (64, 64), color=(33, 150, 243)) 
            
            # Load custom icon
            if os.path.exists("icon.ico"):
                image = PilImage.open("icon.ico")
            menu = (
                pystray.MenuItem(app.lm.t("app_show"), on_tray_open, default=True),
                pystray.MenuItem(app.lm.t("exit"), on_tray_exit)
            )
            icon = pystray.Icon("DynamicScreenBG", image, "Dynamic Screen BG", menu)
            icon.run()
        except Exception as e:
            print(f"Tray error: {e}")

    # Start tray in separate thread
    tray_thread = threading.Thread(target=run_tray, daemon=True)
    tray_thread.start()

    def on_window_event(e):
        if e.data == "close":
            print("Pencere kapatma isteği algılandı, gizleniyor...")
            # We can show a notification here if pystray supports it easily, or just log.
            # Localized console log?
            print(app.lm.t("tray_notification"))
            page.window.visible = False
            page.update()
            
    page.window.on_event = on_window_event
    page.window.prevent_close = True 
    
    icon_path = os.path.join(os.getcwd(), "icon.ico")
    if os.path.exists(icon_path):
        page.window.icon = icon_path
    
    page.update() 

if __name__ == "__main__":
    # Fix for Windows Taskbar Icon
    try:
        import ctypes
        myappid = 'dynamic.screen.bg.v1' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    ft.app(target=main, assets_dir=".")
