import tkinter as tk

class SimpleCalculator:
    # inisialisasi kalkulator
    def __init__(self, root, theme_color):
        self.root = root
        self.theme_color = theme_color  # perintah warna tema

        self.previous_value = "0"   # nilai sebelumnya (jangan diubah)
        self.current_value = "0"    # nilai saat ini (jangan diubah)
        self.operation = None   
        self.should_reset_display = False

        # frame untuk display kalkulator
        self.display_frame = tk.Frame(root, bg=theme_color, height=150)
        self.display_frame.pack(fill=tk.X, padx=10, pady=10)
        self.display_frame.pack_propagate(False)

        # tampilan angka operasi sebelumnya
        self.prev_label = tk.Label(
            self.display_frame,
            text="0",
            bg=theme_color,   # < warna background pada display kalkulator, buat hex color contoh ("#eeeeee") untuk menyesuaikan warna sesuai pilihan sendiri
            fg="#eeeeee",   # < warna teks pada display kalkulator
            font=("Arial", 20, "bold"), # konfigurasi font pada display kalkulator
            anchor="e"
        )
        self.prev_label.pack(fill=tk.X, padx=15, pady=(15, 0))  # < jarak "angka operasi sebelumnya" display kalkulator dari tepi


        # tampilan angka operasi utama
        self.display_label = tk.Label(
            self.display_frame,
            text="0",
            bg=theme_color,   # < warna background pada display kalkulator
            fg="#AFEBF1",   # < warna teks pada display kalkulator
            font=("Arial", 40, "bold"),     # konfigurasi font pada display kalkulator
            anchor="e"
        )
        self.display_label.pack(fill=tk.X, padx=15, pady=(5, 10))   # < jarak "angka operasi utama" display kalkulator dari tepi

        # frame untuk tombol kalkulator
        self.buttons_frame = tk.Frame(root, bg="#C2C9FF")   # < warna background pada tombol kalkulator
        self.buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)    # < jarak tombol kalkulator dari tepi

        # layout tombol kalkulator, bebas diatur sesuai keinginan
        button_layout = [
            ["%", "÷", "C", "⌫"],
            ["1", "2", "3", "−"],
            ["4", "5", "6", "×"],
            ["7", "8", "9", "+"],
            ["0", "", ".", "="]
        ]

    # membuat tombol
        self.buttons = {}
        for row_idx, row in enumerate(button_layout):
            for col_idx, btn_text in enumerate(row):
                if btn_text:
                    self.create_button(btn_text, row_idx, col_idx)

    # fungsi membuat tombol
    def create_button(self, text, row, col):

        # menentukan warna tombol
        if text == "+":             # konfigurasi warna tombol "+", bg_color = background color, fg_color = foreground color (teks)
            bg_color = "#65b2ff"  
            fg_color = "#000000"
        elif text == "−":           # konfigurasi warna tombol "−", bg_color = background color, fg_color = foreground color (teks)
            bg_color = "#65b2ff"  
            fg_color = "#000000"
        elif text == "×":           # konfigurasi warna tombol "×", bg_color = background color, fg_color = foreground color (teks)
            bg_color = "#65b2ff"  
            fg_color = "#000000"
        elif text == "÷":           # konfigurasi warna tombol "÷", bg_color = background color, fg_color = foreground color (teks)
            bg_color = "#65b2ff"  
            fg_color = "#000000"
        elif text == "=":           # konfigurasi warna tombol "=", bg_color = background color, fg_color = foreground color (teks)
            bg_color = "#0A3FBA" 
            fg_color = "#FFFFFF" 
        elif text == "C":           # konfigurasi warna tombol "C", bg_color = background color, fg_color = foreground color (teks)
            bg_color = "#0A3FBA" 
            fg_color = "#FFFFFF"
        elif text == "⌫":          # konfigurasi warna tombol "⌫", bg_color = background color, fg_color = foreground color (teks)
            bg_color = "#0A3FBA"
            fg_color = "#FFFFFF"
        elif text == "%":           # konfigurasi warna tombol "%", bg_color = background color, fg_color = foreground color (teks)
            bg_color = "#65b2ff"
            fg_color = "#000000"
        else:                       # konfigurasi warna tombol angka dan titik, bg_color = background color, fg_color = foreground color (teks)
            bg_color = "#080034"
            fg_color = "#FFFFFF"

        # konfigurasi tombol
        btn = tk.Button(
            self.buttons_frame,
            text=text,
            font=("Arial", 18, "bold"), # < konfigurasi font tombol
            bg=bg_color,
            fg=fg_color,
            activeforeground="#000000", # < warna teks tombol pas ditekan, bisa diatur sesuai pilihan sendiri
            activebackground="#909090", # < warna tombol pas ditekan, bisa diatur sesuai pilihan sendiri
            border=0,
            command=lambda: self.button_click(text)
        )

        # posisi tombol
        if text == "0":
            btn.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=5, pady=5)
        else:
            btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

        self.buttons_frame.grid_rowconfigure(row, weight=1)
        self.buttons_frame.grid_columnconfigure(col, weight=1)

    # fungsi klik operasi perhitungan tombol
    def button_click(self, text):
        if text.isdigit() or text == ".":
            self.append_number(text)
        elif text == "C":
            self.clear()
        elif text == "⌫":
            self.delete_last()
        elif text == "=":
            self.calculate()
        elif text == "%":
            self.percent()
        elif text in ["÷", "×", "−", "+"]:
            self.operation_click(text)

    # menambah angka ke display
    def append_number(self, num):
        if self.should_reset_display:
            self.current_value = str(num)
            self.should_reset_display = False
        else:
            if self.current_value == "0":
                self.current_value = str(num)
            else:
                if not (num == "." in self.current_value):
                    self.current_value += str(num)
        self.update_display()

    # klik operasi perhitungan
    def operation_click(self, op):
        if self.current_value == "":
            return
        if self.previous_value == "0":
            self.previous_value = self.current_value
        elif self.operation:
            result = self.calculate_result(
                float(self.previous_value),
                float(self.current_value),
                self.operation
            )
            self.previous_value = self.format_number(result)
        self.operation = op
        self.should_reset_display = True
        self.update_display()

    # menghitung hasil operasi
    def calculate_result(self, prev, current, op):
        if op == "+":
            return prev + current
        elif op == "−":
            return prev - current
        elif op == "×":
            return prev * current
        elif op == "÷":
            return prev / current if current != 0 else 0
        return 0
    
    # operasi perhitungan "="
    def calculate(self):
        if not self.operation or self.should_reset_display:
            return
        
        # menghitung hasil operasi
        result = self.calculate_result(
            float(self.previous_value),
            float(self.current_value),
            self.operation
        )

        # membatasi hasil hingga 10 desimal
        rounded = round(result, 10)
        self.current_value = self.format_number(rounded)
        self.previous_value = "0"
        self.operation = None
        self.should_reset_display = True
        self.update_display()

    # operasi perhitungan persen "%"
    def percent(self):
        try:
            result = float(self.current_value) / 100
            self.current_value = self.format_number(result)
        except:
            pass
        self.update_display()

    # menghapus semua input angka, "C"
    def clear(self):
        self.previous_value = "0"
        self.current_value = "0"
        self.operation = None
        self.should_reset_display = False
        self.update_display()

    # menghapus angka, "⌫"
    def delete_last(self):
        if len(self.current_value) > 1:
            self.current_value = self.current_value[:-1]
        else:
            self.current_value = "0"
        self.update_display()

    #  update operasi perhitungan ke display
    def update_display(self):
        self.display_label.config(text=self.current_value)
        if self.operation:
            self.prev_label.config(text=f"{self.previous_value} {self.operation}")
        else:
            self.prev_label.config(text=self.previous_value)

    # format angka: hapus trailing .0 dan nol tak perlu setelah desimal
    def format_number(self, num):
        try:
            n = float(num)
        except:
            return str(num)
        # bulatkan dulu ke 10 desimal untuk menghindari floating point noise
        rounded = round(n, 10)
        # format dengan fixed 10 desimal lalu strip trailing zeros dan titik desimal jika perlu
        s = ('{:.10f}'.format(rounded)).rstrip('0').rstrip('.')
        return s if s != '' else '0'

# menjalankan aplikasi kalkulator
if __name__ == "__main__":
    root = tk.Tk()
    root.title("KalkulatorEd") # < tampilan judul aplikasi kalkulator diatas
    root.geometry("350x550")    # ukuran awal kalkulator
    root.config(bg="#909090")   # < warna background utama
    root.resizable(True, True)  # < ukuran kalkulator bisa di ubah "(False, False)" untuk ukuran gak bisa diubah, "(True, True)" untuk bisa diubah
    calc = SimpleCalculator(root, theme_color="#1C2674") # < warna tema

    root.mainloop()