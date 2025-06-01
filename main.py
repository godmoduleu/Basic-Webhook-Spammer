import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
import os
import time
import threading
import json
from io import BytesIO
from PIL import Image, ImageTk

class 迪斯科德网络钩子发送器:
    def __init__(self):
        self.窗口 = tk.Tk()
        self.窗口.title("Discord Webhook Spammer")
        self.窗口.geometry("1024x1024") 
        self.窗口.configure(bg="#1E2124")
        self.窗口.resizable(False, False)
        
        self.发送状态 = False
        self.发送线程 = None
        
        self.图片变量 = tk.StringVar()
        self.艾特变量 = tk.BooleanVar()
        self.名称变量 = tk.StringVar()
        self.头像图片变量 = tk.StringVar()
        self.颜色变量 = tk.StringVar(value="#5865F2")
        self.嵌入标题变量 = tk.StringVar()
        self.嵌入描述变量 = tk.StringVar()
        self.启用嵌入变量 = tk.BooleanVar()
        self.延迟变量 = tk.StringVar(value="0.8")
        
        self.创建界面()
        
    def 创建界面(self):
        标题样式 = {"bg": "#1E2124", "fg": "#FFFFFF", "font": ("Segoe UI", 12, "bold")}
        输入样式 = {
            "bg": "#2C2F33", "fg": "#FFFFFF", "insertbackground": "#FFFFFF",
            "relief": "flat", "borderwidth": 2, "highlightthickness": 1,
            "highlightbackground": "#5865F2", "highlightcolor": "#5865F2"
        }
        按钮样式 = {
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
        
        主框架 = tk.Frame(self.窗口, bg="#1E2124", highlightbackground="#2C2F33", 
                             highlightthickness=2)
        主框架.pack(fill="both", expand=True, padx=20, pady=20)
        
        标签控件 = ttk.Notebook(主框架)
        主标签页 = tk.Frame(标签控件, bg="#1E2124")
        嵌入标签页 = tk.Frame(标签控件, bg="#1E2124")
        
        标签控件.add(主标签页, text="Main Settings")
        标签控件.add(嵌入标签页, text="Embed Settings")
        标签控件.pack(expand=1, fill="both", pady=(0, 10))
        
        tk.Label(主标签页, text="Webhook URL:", **标题样式).pack(fill="x", pady=(15, 5))
        self.输入链接 = tk.Entry(主标签页, **输入样式)
        self.输入链接.pack(fill="x", ipady=6, pady=2)
        
        tk.Label(主标签页, text="Webhook Name:", **标题样式).pack(fill="x", pady=(10, 5))
        tk.Entry(主标签页, textvariable=self.名称变量, **输入样式).pack(fill="x", ipady=6, pady=2)
        
        tk.Label(主标签页, text="Avatar URL:", **标题样式).pack(fill="x", pady=(10, 5))
        头像图片框架 = tk.Frame(主标签页, bg="#1E2124")
        头像图片框架.pack(fill="x")
        tk.Entry(头像图片框架, textvariable=self.头像图片变量, 
                **输入样式).pack(side="left", fill="x", expand=True, ipady=6, pady=2)
        tk.Button(头像图片框架, text="Browse", command=self.选择头像图片, 
                 **按钮样式, width=10).pack(side="right", padx=5)
        
        tk.Label(主标签页, text="Message Content:", **标题样式).pack(fill="x", pady=(10, 5))
        self.消息输入 = tk.Text(主标签页, height=6, **输入样式)
        self.消息输入.pack(fill="x", pady=2)
        
        tk.Label(主标签页, text="Add Image (optional):", **标题样式).pack(fill="x", pady=(10, 5))
        图片框架 = tk.Frame(主标签页, bg="#1E2124")
        图片框架.pack(fill="x")
        tk.Entry(图片框架, textvariable=self.图片变量, **输入样式).pack(side="left", 
                fill="x", expand=True, ipady=6, pady=2)
        tk.Button(图片框架, text="Browse", command=self.选择图片, **按钮样式, 
                 width=10).pack(side="right", padx=5)
        
        tk.Label(主标签页, text="Number of Sends:", **标题样式).pack(fill="x", pady=(10, 5))
        self.发送次数输入 = tk.Entry(主标签页, **输入样式)
        self.发送次数输入.pack(fill="x", ipady=6, pady=2)
        
        tk.Label(主标签页, text="Delay (seconds):", **标题样式).pack(fill="x", pady=(10, 5))
        self.延迟输入 = tk.Entry(主标签页, textvariable=self.延迟变量, **输入样式)
        self.延迟输入.pack(fill="x", ipady=6, pady=2)
        
        艾特按钮 = tk.Checkbutton(主标签页, text="Add @everyone and @here", 
                                variable=self.艾特变量, bg="#1E2124", fg="#FFFFFF", 
                                selectcolor="#2C2F33", activebackground="#1E2124",
                                font=("Segoe UI", 10), activeforeground="#FFFFFF")
        艾特按钮.pack(pady=10)
        
        嵌入按钮 = tk.Checkbutton(嵌入标签页, text="Use Embed", 
                                 variable=self.启用嵌入变量, bg="#1E2124", fg="#FFFFFF", 
                                 selectcolor="#2C2F33", activebackground="#1E2124",
                                 font=("Segoe UI", 10), activeforeground="#FFFFFF")
        嵌入按钮.pack(pady=10)
        
        tk.Label(嵌入标签页, text="Embed Color:", **标题样式).pack(fill="x", pady=(10, 5))
        颜色框架 = tk.Frame(嵌入标签页, bg="#1E2124")
        颜色框架.pack(fill="x")
        颜色输入 = tk.Entry(颜色框架, textvariable=self.颜色变量, **输入样式)
        颜色输入.pack(side="left", fill="x", expand=True, ipady=6, pady=2)
        颜色展示 = tk.Frame(颜色框架, bg="#5865F2", width=40, height=25, 
                             relief="flat", highlightbackground="#2C2F33", 
                             highlightthickness=1)
        颜色展示.pack(side="right", padx=5)
        
        def 更新颜色(event):
            try:
                color = self.颜色变量.get()
                颜色展示.configure(bg=color)
            except:
                pass
        
        颜色输入.bind("<KeyRelease>", 更新颜色)
        
        tk.Label(嵌入标签页, text="Embed Title:", **标题样式).pack(fill="x", pady=(10, 5))
        tk.Entry(嵌入标签页, textvariable=self.嵌入标题变量, **输入样式).pack(fill="x", ipady=6, pady=2)
        
        tk.Label(嵌入标签页, text="Embed Description:", **标题样式).pack(fill="x", pady=(10, 5))
        self.嵌入描述输入 = tk.Text(嵌入标签页, height=8, **输入样式)
        self.嵌入描述输入.pack(fill="x", pady=2)
        
        按钮框架 = tk.Frame(self.窗口, bg="#1E2124")
        按钮框架.pack(fill="x", pady=15)
        
        self.发送按钮 = tk.Button(按钮框架, text="Send", command=self.单次发送, 
                                 **按钮样式, width=15)
        self.发送按钮.pack(side="left", padx=10)
        self.发送按钮.bind("<Enter>", lambda e: self.发送按钮.config(bg="#677BC4"))
        self.发送按钮.bind("<Leave>", lambda e: self.发送按钮.config(bg="#5865F2"))
        
        self.刷屏按钮 = tk.Button(按钮框架, text="Start Spam", command=self.开始刷屏, 
                                **按钮样式, width=15)
        self.刷屏按钮.pack(side="right", padx=10)
        self.刷屏按钮.bind("<Enter>", lambda e: self.刷屏按钮.config(bg="#677BC4"))
        self.刷屏按钮.bind("<Leave>", lambda e: self.刷屏按钮.config(bg="#5865F2"))
        
        self.状态栏 = tk.Label(self.窗口, text="Ready", bd=0, relief=tk.FLAT, anchor=tk.W,
                                    bg="#2C2F33", fg="#B9BBBE", font=("Segoe UI", 10),
                                    height=2)
        self.状态栏.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
    
    def 选择图片(self):
        文件 = filedialog.askopenfilename(
            title="Select Image", 
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.webp")]
        )
        if 文件:
            self.图片变量.set(文件)
    
    def 选择头像图片(self):
        文件 = filedialog.askopenfilename(
            title="Select Avatar Image", 
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.webp")]
        )
        if 文件:
            self.头像图片变量.set(文件)
    
    def 创建数据(self):
        webhook_url = self.输入链接.get().strip()
        message = self.消息输入.get("1.0", tk.END).strip()
        webhook_name = self.名称变量.get().strip()
        avatar_url = self.头像图片变量.get().strip()
        image_path = self.图片变量.get().strip()
        ping_enabled = self.艾特变量.get()
        embed_enabled = self.启用嵌入变量.get()
        
        if not webhook_url:
            messagebox.showerror("Error", "Webhook URL cannot be empty!")
            return None, None
        
        webhook_data = {}
        
        if webhook_name:
            webhook_data["username"] = webhook_name
        
        if avatar_url:
            if os.path.isfile(avatar_url):
                self.状态栏.config(text="Note: Local avatar files cannot be used directly in webhook")
            else:
                webhook_data["avatar_url"] = avatar_url
        
        content = ""
        if ping_enabled:
            content = "@everyone @here"
        if message and not embed_enabled:
            if content:
                content += "\n" + message
            else:
                content = message
        webhook_data["content"] = content
        
        if embed_enabled:
            embed = {
                "title": self.嵌入标题变量.get().strip(),
                "description": self.嵌入描述输入.get("1.0", tk.END).strip(),
                "color": int(self.颜色变量.get().lstrip('#'), 16) if self.颜色变量.get().startswith('#') else int(self.颜色变量.get())
            }
            webhook_data["embeds"] = [embed]
        
        if image_path:
            if os.path.isfile(image_path):
                try:
                    with open(image_path, "rb") as f:
                        file_data = f.read()
                    webhook_data["files"] = {"image": (os.path.basename(image_path), file_data)}
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load image file: {e}")
            else:
                # Image URL maybe
                if "embeds" not in webhook_data:
                    webhook_data["embeds"] = []
                webhook_data["embeds"].append({"image": {"url": image_path}})
        
        return webhook_url, webhook_data
    
    def 发送消息(self):
        webhook_url, data = self.创建数据()
        if webhook_url is None:
            return False
        
        try:
            headers = {
                "Content-Type": "application/json"
            }
            # 直接用requests发送数据，排除files，因为Webhook标准库通常不支持文件
            resp = requests.post(webhook_url, json=data)
            if resp.status_code in (200, 204):
                self.状态栏.config(text="Message sent successfully")
                return True
            else:
                self.状态栏.config(text=f"Error sending message: {resp.status_code}")
                return False
        except Exception as e:
            self.状态栏.config(text=f"Error: {str(e)}")
            return False
    
    def 单次发送(self):
        self.发送消息()
    
    def 开始刷屏(self):
        if self.发送状态:
            self.发送状态 = False
            self.刷屏按钮.config(text="Start Spam")
            self.发送按钮.config(state="normal")
            self.状态栏.config(text="Spam stopped.")
            return
        
        try:
            发送次数 = int(self.发送次数输入.get())
            if 发送次数 <= 0:
                messagebox.showerror("Error", "Send count must be greater than 0.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid number of sends.")
            return
        
        try:
            延迟 = float(self.延迟变量.get())
            if 延迟 < 0:
                messagebox.showerror("Error", "Delay cannot be negative.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid delay.")
            return
        
        self.发送状态 = True
        self.刷屏按钮.config(text="Stop Spam")
        self.发送按钮.config(state="disabled")
        self.发送线程 = threading.Thread(target=self.刷屏循环, args=(发送次数, 延迟), daemon=True)
        self.发送线程.start()
    
    def 刷屏循环(self, count, delay):
        for i in range(count):
            if not self.发送状态:
                break
            成功 = self.发送消息()
            if not 成功:
                break
            self.状态栏.config(text=f"Sent {i+1}/{count}")
            time.sleep(delay)
        self.发送状态 = False
        self.刷屏按钮.config(text="Start Spam")
        self.发送按钮.config(state="normal")
        self.状态栏.config(text="Spam finished.")
    
    def 运行(self):
        self.窗口.mainloop()

if __name__ == "__main__":
    app = 迪斯科德网络钩子发送器()
    app.运行()
