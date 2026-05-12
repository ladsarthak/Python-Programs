from plyer import notification

def desktop_notifier(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Desktop Notifier",
        timeout=10
    )

if __name__ == "__main__":
    desktop_notifier("Hello!", "This is Sarthak's Desktop!")