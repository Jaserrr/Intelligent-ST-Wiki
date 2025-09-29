import tkinter as tk
from PIL import Image, ImageTk
import random
import time

class LotteryApp:
    def __init__(self, master):
        self.master = master  # 初始化主窗口
        self.master.title("Genshin Impact Wish System —— HDU Ver.") 
        image = Image.open("hduqd.png") 
        photo = ImageTk.PhotoImage(image)  # 使用ImageTk模块创建图片对象
        self.startup_label = tk.Label(self.master, image=photo)  # 创建标签并显示图片
        self.startup_label.image = photo  # 保持引用，防止被垃圾回收
        self.startup_label.pack()  # 将标签放置到主窗口上
        # 延时两秒后调用显示抽奖页面
        self.master.after(2000, self.show_lottery_page)  # 在2000ms后调用show_lottery_page方法
        self.stone_count = 1600  # 初始化原石数量
        self.stone_label = tk.Label(self.master, text=f"原石：{self.stone_count}", font=("宋体", 20))  # 创建标签显示原石数量
        self.stone_label.place(x=1300, y=50)  # 设置标签位置

    def show_lottery_page(self):
        self.startup_label.destroy()  # 销毁启动图片
        self.label = tk.Label(self.master, fg='red', text="恭喜您获得：", font=("宋体", 40))  # 创建标签显示祝贺信息
        self.label.pack(pady=100)  # 将标签放置到主窗口上
        self.result_var = tk.StringVar()  # 创建变量对象用于显示抽奖结果
        self.result_label = tk.Label(self.master, textvariable=self.result_var, font=("等线", 90))  # 创建标签显示抽奖结果
        self.result_label.pack()  # 将标签放置到主窗口上
        self.lottery_button = tk.Button(self.master, bg='lightgreen', text="祈愿1次（原石*160）", command=self.draw_lottery, font=("宋体", 14))  # 创建按钮用于执行抽奖操作
        self.lottery_button.pack(pady=100)  # 将按钮放置到主窗口上

    def draw_lottery(self):
        cost = 160  # 每次祈愿消耗160原石
        if self.stone_count >= cost:  # 如果剩余原石足够
            candidates = ["PKU录取通知书", "THU录取通知书", "ZJU录取通知书", "SJTU录取通知书","HDU再读十年书"]  # 卡池具体内容
            winner = random.choice(candidates)  # 随机抽取获奖者
            self.result_var.set(winner)  # 设置抽奖结果
            # 更新原石数量
            self.stone_count -= cost  # 扣除抽奖消耗的原石
            self.stone_label.config(text=f"原石：{self.stone_count}")  # 更新原石数量显示
        else:  # 如果原石不足
            # 如果原石不足，弹出提示框
            tk.messagebox.showinfo("提示", "原石不足，建议充值¥648！")

if __name__ == "__main__":
    root = tk.Tk()  # 创建主窗口
    root.geometry('1600x900-150-100')  # 设置主窗口大小和位置
    app = LotteryApp(root)  # 创建抽奖应用实例
    root.mainloop()  # 运行主程序
