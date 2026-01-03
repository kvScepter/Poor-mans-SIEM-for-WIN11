from win11toast import toast

class Notifier:
    def send_alert(self, title, message):
        try:
            # Käytetään tyhjää callbackia estämään konsolin tulosteet
            toast(title, message, duration='short', on_dismissed=lambda args: None)
        except: pass
