import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
import os
import time
import threading
import json
from io import BytesIO
from PIL import Image, ImageTk

class مرسل_ويب_هوك_ديسكورد:
    def __init__(self):
        self.نافذة = tk.Tk()
        self.نافذة.title("Discord Webhook Spammer")
        self.نافذة.geometry("1024x1024") 
        self.نافذة.configure(bg="#1E2124")
        self.نافذة.resizable(False, False)
        
        self.حالة_السبام = False
        self.خيط_السبام = None
        
        self.متغير_الصورة = tk.StringVar()
        self.متغير_بينج = tk.BooleanVar()
        self.متغير_الاسم = tk.StringVar()
        self.متغير_الصورة_الرمزية = tk.StringVar()
        self.متغير_اللون = tk.StringVar(value="#5865F2")
        self.متغير_عنوان_الامبد = tk.StringVar()
        self.متغير_وصف_الامبد = tk.StringVar()
        self.متغير_تفعيل_الامبد = tk.BooleanVar()
        self.متغير_التأخير = tk.StringVar(value="0.8")
        
        self.إنشاء_واجهة()
        
    def إنشاء_واجهة(self):
        نمط_العنوان = {"bg": "#1E2124", "fg": "#FFFFFF", "font": ("Segoe UI", 12, "bold")}
        نمط_الإدخال = {
            "bg": "#2C2F33", "fg": "#FFFFFF", "insertbackground": "#FFFFFF",
            "relief": "flat", "borderwidth": 2, "highlightthickness": 1,
            "highlightbackground": "#5865F2", "highlightcolor": "#5865F2"
        }
        نمط_الزر = {
            "bg": "#5865F2", "fg": "#FFFFFF", "activebackground": "#4752C4",
            "activeforeground": "#FFFFFF", "relief": "flat",
            "font": ("Segoe UI", 10, "bold"), "borderwidth": 0
        }
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#1E2124", borderwidth=0)
        style.configure("TNotebook.Tab", 
                       background="#2C2F33", 
                       foreground="#FFFFFF", 
                       padding=[15, 8], 
                       font=("Segoe UI", 11, "bold"),
                       borderwidth=0)
        style.map("TNotebook.Tab", 
                 background=[("selected", "#5865F2")], 
                 foreground=[("selected", "#FFFFFF")])
        
        إطار_رئيسي = tk.Frame(self.نافذة, bg="#1E2124", highlightbackground="#2C2F33", 
                             highlightthickness=2)
        إطار_رئيسي.pack(fill="both", expand=True, padx=20, pady=20)
        
        تحكم_علامات_التبويب = ttk.Notebook(إطار_رئيسي)
        تبويب_رئيسي = tk.Frame(تحكم_علامات_التبويب, bg="#1E2124")
        تبويب_امبد = tk.Frame(تحكم_علامات_التبويب, bg="#1E2124")
        
        تحكم_علامات_التبويب.add(تبويب_رئيسي, text="Main Settings")
        تحكم_علامات_التبويب.add(تبويب_امبد, text="Embed Settings")
        تحكم_علامات_التبويب.pack(expand=1, fill="both", pady=(0, 10))
        
        tk.Label(تبويب_رئيسي, text="Webhook URL:", **نمط_العنوان).pack(fill="x", pady=(15, 5))
        self.إدخال_الرابط = tk.Entry(تبويب_رئيسي, **نمط_الإدخال)
        self.إدخال_الرابط.pack(fill="x", ipady=6, pady=2)
        
        tk.Label(تبويب_رئيسي, text="Webhook Name:", **نمط_العنوان).pack(fill="x", pady=(10, 5))
        tk.Entry(تبويب_رئيسي, textvariable=self.متغير_الاسم, **نمط_الإدخال).pack(fill="x", ipady=6, pady=2)
        
        tk.Label(تبويب_رئيسي, text="Avatar URL:", **نمط_العنوان).pack(fill="x", pady=(10, 5))
        إطار_الصورة_الرمزية = tk.Frame(تبويب_رئيسي, bg="#1E2124")
        إطار_الصورة_الرمزية.pack(fill="x")
        tk.Entry(إطار_الصورة_الرمزية, textvariable=self.متغير_الصورة_الرمزية, 
                **نمط_الإدخال).pack(side="left", fill="x", expand=True, ipady=6, pady=2)
        tk.Button(إطار_الصورة_الرمزية, text="Browse", command=self.اختيار_صورة_رمزية, 
                 **نمط_الزر, width=10).pack(side="right", padx=5)
        
        tk.Label(تبويب_رئيسي, text="Message Content:", **نمط_العنوان).pack(fill="x", pady=(10, 5))
        self.إدخال_الرسالة = tk.Text(تبويب_رئيسي, height=6, **نمط_الإدخال)
        self.إدخال_الرسالة.pack(fill="x", pady=2)
        
        tk.Label(تبويب_رئيسي, text="Add Image (optional):", **نمط_العنوان).pack(fill="x", pady=(10, 5))
        إطار_الصورة = tk.Frame(تبويب_رئيسي, bg="#1E2124")
        إطار_الصورة.pack(fill="x")
        tk.Entry(إطار_الصورة, textvariable=self.متغير_الصورة, **نمط_الإدخال).pack(side="left", 
                fill="x", expand=True, ipady=6, pady=2)
        tk.Button(إطار_الصورة, text="Browse", command=self.اختيار_صورة, **نمط_الزر, 
                 width=10).pack(side="right", padx=5)
        
        tk.Label(تبويب_رئيسي, text="Number of Sends:", **نمط_العنوان).pack(fill="x", pady=(10, 5))
        self.إدخال_العدد = tk.Entry(تبويب_رئيسي, **نمط_الإدخال)
        self.إدخال_العدد.pack(fill="x", ipady=6, pady=2)
        
        tk.Label(تبويب_رئيسي, text="Delay (seconds):", **نمط_العنوان).pack(fill="x", pady=(10, 5))
        self.إدخال_التأخير = tk.Entry(تبويب_رئيسي, textvariable=self.متغير_التأخير, **نمط_الإدخال)
        self.إدخال_التأخير.pack(fill="x", ipady=6, pady=2)
        
        زر_بينج = tk.Checkbutton(تبويب_رئيسي, text="Add @everyone and @here", 
                                variable=self.متغير_بينج, bg="#1E2124", fg="#FFFFFF", 
                                selectcolor="#2C2F33", activebackground="#1E2124",
                                font=("Segoe UI", 10), activeforeground="#FFFFFF")
        زر_بينج.pack(pady=10)
        
        زر_امبد = tk.Checkbutton(تبويب_امبد, text="Use Embed", 
                                 variable=self.متغير_تفعيل_الامبد, bg="#1E2124", fg="#FFFFFF", 
                                 selectcolor="#2C2F33", activebackground="#1E2124",
                                 font=("Segoe UI", 10), activeforeground="#FFFFFF")
        زر_امبد.pack(pady=10)
        
        tk.Label(تبويب_امبد, text="Embed Color:", **نمط_العنوان).pack(fill="x", pady=(10, 5))
        إطار_اللون = tk.Frame(تبويب_امبد, bg="#1E2124")
        إطار_اللون.pack(fill="x")
        حقل_اللون = tk.Entry(إطار_اللون, textvariable=self.متغير_اللون, **نمط_الإدخال)
        حقل_اللون.pack(side="left", fill="x", expand=True, ipady=6, pady=2)
        عرض_اللون = tk.Frame(إطار_اللون, bg="#5865F2", width=40, height=25, 
                             relief="flat", highlightbackground="#2C2F33", 
                             highlightthickness=1)
        عرض_اللون.pack(side="right", padx=5)
        
        def تحديث_اللون(event):
            try:
                لون = self.متغير_اللون.get()
                عرض_اللون.configure(bg=لون)
            except:
                pass
        
        حقل_اللون.bind("<KeyRelease>", تحديث_اللون)
        
        tk.Label(تبويب_امبد, text="Embed Title:", **نمط_العنوان).pack(fill="x", pady=(10, 5))
        tk.Entry(تبويب_امبد, textvariable=self.متغير_عنوان_الامبد, **نمط_الإدخال).pack(fill="x", ipady=6, pady=2)
        
        tk.Label(تبويب_امبد, text="Embed Description:", **نمط_العنوان).pack(fill="x", pady=(10, 5))
        self.وصف_الامبد = tk.Text(تبويب_امبد, height=8, **نمط_الإدخال)
        self.وصف_الامبد.pack(fill="x", pady=2)
        
        إطار_الأزرار = tk.Frame(self.نافذة, bg="#1E2124")
        إطار_الأزرار.pack(fill="x", pady=15)
        
        self.زر_إرسال = tk.Button(إطار_الأزرار, text="Send", command=self.إرسال_مرة_واحدة, 
                                 **نمط_الزر, width=15)
        self.زر_إرسال.pack(side="left", padx=10)
        self.زر_إرسال.bind("<Enter>", lambda e: self.زر_إرسال.config(bg="#677BC4"))
        self.زر_إرسال.bind("<Leave>", lambda e: self.زر_إرسال.config(bg="#5865F2"))
        
        self.زر_سبام = tk.Button(إطار_الأزرار, text="Start Spam", command=self.بدء_السبام, 
                                **نمط_الزر, width=15)
        self.زر_سبام.pack(side="right", padx=10)
        self.زر_سبام.bind("<Enter>", lambda e: self.زر_سبام.config(bg="#677BC4"))
        self.زر_سبام.bind("<Leave>", lambda e: self.زر_سبام.config(bg="#5865F2"))
        
        self.شريط_الحالة = tk.Label(self.نافذة, text="Ready", bd=0, relief=tk.FLAT, anchor=tk.W,
                                    bg="#2C2F33", fg="#B9BBBE", font=("Segoe UI", 10),
                                    height=2)
        self.شريط_الحالة.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
    
    def اختيار_صورة(self):
        ملف = filedialog.askopenfilename(
            title="Select Image", 
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.webp")]
        )
        if ملف:
            self.متغير_الصورة.set(ملف)
    
    def اختيار_صورة_رمزية(self):
        ملف = filedialog.askopenfilename(
            title="Select Avatar Image", 
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.webp")]
        )
        if ملف:
            self.متغير_الصورة_الرمزية.set(ملف)
    
    def إنشاء_البيانات(self):
        رابط_الويب_هوك = self.إدخال_الرابط.get().strip()
        رسالة = self.إدخال_الرسالة.get("1.0", tk.END).strip()
        اسم_الويب_هوك = self.متغير_الاسم.get().strip()
        رابط_الصورة_الرمزية = self.متغير_الصورة_الرمزية.get().strip()
        مسار_الصورة = self.متغير_الصورة.get().strip()
        متغير_بينج = self.متغير_بينج.get()
        متغير_امبد = self.متغير_تفعيل_الامبد.get()
        
        if not رابط_الويب_هوك:
            messagebox.showerror("Error", "Webhook URL cannot be empty!")
            return None, None
        
        بيانات_الويب_هوك = {}
        
        if اسم_الويب_هوك:
            بيانات_الويب_هوك["username"] = اسم_الويب_هوك
        
        if رابط_الصورة_الرمزية:
            if os.path.isfile(رابط_الصورة_الرمزية):
                self.شريط_الحالة.config(text="Note: Local avatar files cannot be used directly in webhook")
            else:
                بيانات_الويب_هوك["avatar_url"] = رابط_الصورة_الرمزية
        
        محتوى = ""
        if متغير_بينج:
            محتوى = "@everyone @here"
        if رسالة and not متغير_امبد:
            if محتوى:
                محتوى += "\n" + رسالة
            else:
                محتوى = رسالة
        بيانات_الويب_هوك["content"] = محتوى
        
        if متغير_امبد:
            امبد = {
                "title": self.متغير_عنوان_الامبد.get().strip(),
                "description": self.وصف_الامبد.get("1.0", tk.END).strip(),
                "color": int(self.متغير_اللون.get().lstrip('#'), 16) if self.متغير_اللون.get().startswith('#') else int(self.متغير_اللون.get())
            }
            بيانات_الويب_هوك["embeds"] = [امبد]
        
        return بيانات_الويب_هوك, مسار_الصورة
    
    def إرسال_الرسائل(self, بيانات_الويب_هوك, مسار_الصورة, عدد=1, وضع_السبام=False):
        رابط_الويب_هوك = self.إدخال_الرابط.get().strip()
        try:
            تأخير = float(self.متغير_التأخير.get().strip())
            if تأخير < 0.1:
                تأخير = 0.1
        except:
            messagebox.showerror("Error", "Please enter a valid delay (minimum 0.1 seconds).")
            return 0
        
        نجاح = 0
        for i in range(عدد):
            if not وضع_السبام and not self.حالة_السبام:
                break
                
            ملفات = None
            if مسار_الصورة and os.path.isfile(مسار_الصورة):
                ملفات = {"file": open(مسار_الصورة, "rb")}
                
            try:
                استجابة = requests.post(رابط_الويب_هوك, json=بيانات_الويب_هوك, files=ملفات)
                if استجابة.status_code in [200, 204]:
                    نجاح += 1
                    self.شريط_الحالة.config(text=f"Message sent ({نجاح}/{عدد})")
                else:
                    self.شريط_الحالة.config(text=f"Error: HTTP {استجابة.status_code} - {استجابة.text}")
                    time.sleep(2)
            except Exception as خطأ:
                self.شريط_الحالة.config(text=f"Error: {str(خطأ)}")
                time.sleep(2)
            finally:
                if ملفات:
                    ملفات["file"].close()
            
            time.sleep(تأخير)
        
        if not وضع_السبام:
            self.شريط_الحالة.config(text=f"Completed: {نجاح}/{عدد} messages sent successfully")
            messagebox.showinfo("Completed", f"{نجاح}/{عدد} messages sent successfully.")
        
        return نجاح
    
    def إرسال_مرة_واحدة(self):
        try:
            عدد = int(self.إدخال_العدد.get().strip())
            if عدد <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Please enter a valid positive number.")
            return
        
        بيانات_الويب_هوك, مسار_الصورة = self.إنشاء_البيانات()
        if بيانات_الويب_هوك:
            self.إرسال_الرسائل(بيانات_الويب_هوك, مسار_الصورة, عدد)
    
    def بدء_السبام(self):
        if self.حالة_السبام:
            self.حالة_السبام = False
            self.زر_سبام.config(text="Start Spam")
            self.زر_إرسال.config(state="normal")
            self.شريط_الحالة.config(text="Spam stopped")
            return
        
        بيانات_الويب_هوك, مسار_الصورة = self.إنشاء_البيانات()
        if not بيانات_الويب_هوك:
            return
        
        self.حالة_السبام = True
        self.زر_سبام.config(text="Stop")
        self.زر_إرسال.config(state="disabled")
        
        def خيط_السبام():
            عداد = 0
            while self.حالة_السبام:
                نجاح = self.إرسال_الرسائل(بيانات_الويب_هوك, مسار_الصورة, 1, True)
                عداد += نجاح
                self.شريط_الحالة.config(text=f"Spam ongoing: {عداد} messages sent")
        
        self.خيط_السبام = threading.Thread(target=خيط_السبام)
        self.خيط_السبام.daemon = True
        self.خيط_السبام.start()

if __name__ == "__main__":
    تطبيق = مرسل_ويب_هوك_ديسكورد()
    تطبيق.نافذة.mainloop()