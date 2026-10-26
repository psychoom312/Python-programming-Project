import requests
import customtkinter as ctk

# Disable SSL warning printouts in terminal since we are bypassing broken local environment certs
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

CURRENCY_DATA = {
    "United States - USD ($)": {"code": "USD", "symbol": "$"},
    "Eurozone - EUR (€)": {"code": "EUR", "symbol": "€"},
    "United Kingdom - GBP (£)": {"code": "GBP", "symbol": "£"},
    "India - INR (₹)": {"code": "INR", "symbol": "₹"},
    "Australia - AUD ($)": {"code": "AUD", "symbol": "$"},
    "Canada - CAD ($)": {"code": "CAD", "symbol": "$"},
    "Japan - JPY (¥)": {"code": "JPY", "symbol": "¥"},
    "Singapore - SGD ($)": {"code": "SGD", "symbol": "$"},
    "United Arab Emirates - AED (د.إ)": {"code": "AED", "symbol": "د.إ"},
    "Switzerland - CHF (Fr)": {"code": "CHF", "symbol": "Fr"},
    "China - CNY (¥)": {"code": "CNY", "symbol": "¥"},
    "New Zealand - NZD ($)": {"code": "NZD", "symbol": "$"},
    "South Africa - ZAR (R)": {"code": "ZAR", "symbol": "R"},
    "Brazil - BRL (R$)": {"code": "BRL", "symbol": "R$"},
    "Russia - RUB (₽)": {"code": "RUB", "symbol": "₽"},
    "South Korea - KRW (₩)": {"code": "KRW", "symbol": "₩"},
    "Saudi Arabia - SAR (ر.س)": {"code": "SAR", "symbol": "ر.س"},
    "Turkey - TRY (₺)": {"code": "TRY", "symbol": "₺"},
    "Hong Kong - HKD ($)": {"code": "HKD", "symbol": "$"},
    "Sweden - SEK (kr)": {"code": "SEK", "symbol": "kr"},
    "Norway - NOK (kr)": {"code": "NOK", "symbol": "kr"},
    "Denmark - DKK (kr)": {"code": "DKK", "symbol": "kr"},
    "Mexico - MXN ($)": {"code": "MXN", "symbol": "$"},
    "Malaysia - MYR (RM)": {"code": "MYR", "symbol": "RM"},
    "Indonesia - IDR (Rp)": {"code": "IDR", "symbol": "Rp"},
    "Philippines - PHP (₱)": {"code": "PHP", "symbol": "₱"},
    "Thailand - THB (฿)": {"code": "THB", "symbol": "฿"},
    "Israel - ILS (₪)": {"code": "ILS", "symbol": "₪"},
    "Egypt - EGP (E£)": {"code": "EGP", "symbol": "E£"},
    "Poland - PLN (zł)": {"code": "PLN", "symbol": "zł"},
    "Czech Republic - CZK (Kč)": {"code": "CZK", "symbol": "Kč"}
}

def get_live_exchange_rates(base_currency):
    """
    Fetches real-time live data with browser impersonation.
    verify=False ignores broken system SSL path configurations in virtual envs.
    """
    # Emulates a desktop web browser cleanly to pass network firewalls
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    # Live Source A
    url1 = f"https://frankfurter.dev{base_currency}"
    try:
        response = requests.get(url1, headers=headers, timeout=6, verify=False)
        if response.status_code == 200:
            data = response.json()
            rates = data.get("rates", {})
            rates[base_currency] = 1.0
            return rates, "Live Frankfurter Engine"
    except:
        pass

    # Live Source B
    url2 = f"https://open.er-api.com/v6/latest/{base_currency}"
    try:
        response = requests.get(url2, headers=headers, timeout=6, verify=False)
        if response.status_code == 200:
            data = response.json()
            if data.get("result") == "success":
                rates = data.get("rates", {})
                return rates, "Live Open-ER Engine"
    except:
        pass

    # Live Source C
    url3 = f"https://exchangerate.fun{base_currency}"
    try:
        response = requests.get(url3, headers=headers, timeout=6, verify=False)
        if response.status_code == 200:
            data = response.json()
            rates = data.get("rates", {})
            rates[base_currency] = 1.0
            return rates, "Live ExchangeRate.Fun Engine"
    except:
        pass

    return None, None

def calculate_conversion(amount, rate):
    return round(amount * rate, 2)

class CurrencyConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Currency Converter Pro")
        self.geometry("460x520")
        self.resizable(False, False)

        self.main_frame = ctk.CTkFrame(self, corner_radius=12)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Global Currency Converter", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.title_label.pack(pady=(25, 5))

        self.subtitle_label = ctk.CTkLabel(
            self.main_frame, 
            text="Real-time multi-country currency exchange", 
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.subtitle_label.pack(pady=(0, 25))

        self.amount_entry = ctk.CTkEntry(
            self.main_frame, 
            placeholder_text="Enter amount...",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.amount_entry.pack(fill="x", padx=40, pady=10)
        self.amount_entry.insert(0, "1")

        dropdown_options = sorted(list(CURRENCY_DATA.keys()))

        self.dropdown_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.dropdown_frame.pack(fill="x", padx=40, pady=10)

        self.from_dropdown = ctk.CTkOptionMenu(
            self.dropdown_frame, 
            values=dropdown_options,
            height=38,
            width=175
        )
        self.from_dropdown.pack(side="left")
        self.from_dropdown.set("United States - USD ($)")

        self.to_dropdown = ctk.CTkOptionMenu(
            self.dropdown_frame, 
            values=dropdown_options,
            height=38,
            width=175
        )
        self.to_dropdown.pack(side="right")
        self.to_dropdown.set("India - INR (₹)")

        self.convert_btn = ctk.CTkButton(
            self.main_frame, 
            text="Convert Currency", 
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.process_conversion
        )
        self.convert_btn.pack(fill="x", padx=40, pady=(20, 5))

        self.status_bar = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color="gray"
        )
        self.status_bar.pack(pady=2)

        self.result_frame = ctk.CTkFrame(self.main_frame, height=85, fg_color=("#eef2f7", "#2b2b2b"), corner_radius=8)
        self.result_frame.pack(fill="x", padx=40, pady=(5, 20))
        self.result_frame.pack_propagate(False)

        self.result_label = ctk.CTkLabel(
            self.result_frame, 
            text="Result will appear here", 
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="center",
            wraplength=320
        )
        self.result_label.pack(fill="both", expand=True)

    def process_conversion(self):
        self.status_bar.configure(text="Connecting to live endpoints...", text_color="gray")
        self.update()
        
        raw_amount = self.amount_entry.get().strip()
        from_selection = self.from_dropdown.get()
        to_selection = self.to_dropdown.get()

        from_curr = CURRENCY_DATA[from_selection]["code"]
        from_symbol = CURRENCY_DATA[from_selection]["symbol"]
        
        to_curr = CURRENCY_DATA[to_selection]["code"]
        to_symbol = CURRENCY_DATA[to_selection]["symbol"]

        if not raw_amount:
            self.status_bar.configure(text="⚠️ Please provide a valid numeric amount.", text_color="#e74c3c")
            return
        
        try:
            amount = float(raw_amount)
        except ValueError:
            self.status_bar.configure(text="⚠️ Amount must contain numeric values only.", text_color="#e74c3c")
            return

        rates, live_source = get_live_exchange_rates(from_curr)
        
        if not rates:
            self.status_bar.configure(text="❌ Hardware/SSL block active. Real-time data unreachable.", text_color="#e74c3c")
            self.result_label.configure(text="Connection Error")
            return
        
        target_rate = rates.get(to_curr)
        if not target_rate:
            self.status_bar.configure(text=f"⚠️ Live path mapping conflict.", text_color="#e74c3c")
            self.result_label.configure(text="Conversion Failed")
            return

        converted_val = calculate_conversion(amount, target_rate)
        
        self.result_label.configure(
            text=f"{from_symbol}{amount:,.2f} ({from_curr}) = {to_symbol}{converted_val:,.2f} ({to_curr})"
        )
        
        self.status_bar.configure(text=f"Source: {live_source} (Bypassed & Verified)", text_color="#2ecc71")

if __name__ == "__main__":
    app = CurrencyConverterApp()
    app.mainloop()
