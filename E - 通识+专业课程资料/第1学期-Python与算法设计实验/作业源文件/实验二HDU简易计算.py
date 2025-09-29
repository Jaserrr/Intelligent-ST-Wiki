import tkinter as tk
app=tk.Tk()
app.title("简易计算器 by LJX")
input_text=tk.StringVar()
output_text=tk.StringVar()
input_entry=tk.Entry(app, textvariable=input_text, width=20)
input_entry.grid(row=0,column=0,columnspan=4,padx=10,pady=10)
output_label=tk.Label(app,textvariable=output_text,width=20,relief="solid")
output_label.grid(row=1,column=0,columnspan=4,padx=10,pady=10)
def button_click(value):
    current=input_text.get()
    if value=="=":
        try:
            result=eval(current)
            output_text.set(result)
        except:
            output_text.set("错误")
    elif value=="清除":
        input_text.set("")
        output_text.set("")
    else:
        input_text.set(current+value)
buttons=['7','8','9','/','4','5','6','*','1', '2', '3', '-','0','.','=','+','清除']
row,col=2,0
for button in buttons:
    tk.Button(app,text=button,width=8,bg='lightgreen',command=lambda value=button:button_click(value)).grid(row=row,column=col,padx=5,pady=5)
    col+=1
    if col>3:
        col=0
        row+=1
app.mainloop()