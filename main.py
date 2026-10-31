
import socket
import threading
import time
import urllib.request

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window


Window.clearcolor = (0.035, 0.055, 0.08, 1)


class PhoenixMobile(App):

    def build(self):
        self.title = "Phoenix Mobile"

        root = BoxLayout(
            orientation="vertical",
            padding=18,
            spacing=12
        )

        title = Label(
            text="[b]PHOENIX MOBILE[/b]",
            markup=True,
            font_size="26sp",
            color=(0.1, 0.9, 0.75, 1),
            size_hint_y=None,
            height=55
        )
        root.add_widget(title)

        subtitle = Label(
            text="NETWORK DIAGNOSTICS",
            font_size="12sp",
            color=(0.65, 0.75, 0.85, 1),
            size_hint_y=None,
            height=25
        )
        root.add_widget(subtitle)

        self.status = Label(
            text="Ready to diagnose your connection",
            font_size="15sp",
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=65
        )
        root.add_widget(self.status)

        scroll = ScrollView()
        buttons = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None
        )
        buttons.bind(minimum_height=buttons.setter("height"))

        options = [
            ("INTERNET CONNECTION", self.internet_test),
            ("DNS LOOKUP", self.dns_test),
            ("PING TEST", self.ping_test),
            ("PUBLIC IP", self.public_ip),
            ("DOWNLOAD SPEED TEST", self.speed_test),
        ]

        for name, action in options:
            btn = Button(
                text=name,
                size_hint_y=None,
                height=58,
                background_normal="",
                background_color=(0.04, 0.35, 0.34, 1),
                color=(1, 1, 1, 1),
                font_size="14sp"
            )
            btn.bind(on_press=action)
            buttons.add_widget(btn)

        scroll.add_widget(buttons)
        root.add_widget(scroll)

        self.result = Label(
            text="Results will appear here.",
            font_size="13sp",
            color=(0.75, 0.85, 0.9, 1),
            size_hint_y=None,
            height=100
        )
        root.add_widget(self.result)

        return root

    def run_test(self, function):
        self.status.text = "Testing connection..."
        self.result.text = "Please wait..."

        def worker():
            try:
                message = function()
            except Exception as error:
                message = "Error: " + str(error)

            Clock.schedule_once(
                lambda dt: self.show_result(message)
            )

        threading.Thread(target=worker, daemon=True).start()

    def show_result(self, message):
        self.status.text = "Test completed"
        self.result.text = message

    def internet_test(self, instance):
        self.run_test(self.check_internet)

    def check_internet(self):
        request = urllib.request.Request(
            "https://example.com",
            headers={"User-Agent": "PhoenixMobile"}
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            return "Internet connection: OK\nHTTP status: " + str(response.status)

    def dns_test(self, instance):
        self.run_test(self.check_dns)

    def check_dns(self):
        addresses = socket.getaddrinfo(
            "google.com", 443,
            type=socket.SOCK_STREAM
        )
        ip = addresses[0][4][0]
        return "DNS lookup successful\nGoogle IP: " + ip

    def ping_test(self, instance):
        self.run_test(self.check_ping)

    def check_ping(self):
        start = time.time()
        connection = socket.create_connection(
            ("1.1.1.1", 443), timeout=8
        )
        connection.close()
        elapsed = (time.time() - start) * 1000
        return "Connection to 1.1.1.1: OK\nResponse time: %.2f ms" % elapsed

    def public_ip(self, instance):
        self.run_test(self.check_public_ip)

    def check_public_ip(self):
        with urllib.request.urlopen(
            "https://api.ipify.org", timeout=10
        ) as response:
            ip = response.read().decode()
        return "Public IP check successful\n" + ip

    def speed_test(self, instance):
        self.run_test(self.check_speed)

    def check_speed(self):
        url = "https://speed.cloudflare.com/__down?bytes=1000000"
        start = time.time()

        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read()

        elapsed = time.time() - start
        mbps = (len(data) * 8) / elapsed / 1000000

        return (
            "Download test completed\n"
            "Downloaded: %.2f MB\n"
            "Speed: %.2f Mbps" %
            (len(data) / 1000000, mbps)
        )


if __name__ == "__main__":
    PhoenixMobile().run()
