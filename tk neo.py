import tkinter
from tkinter import messagebox
from tkinter.constants import DISABLED, END, HORIZONTAL

from transformers import GPTNeoForCausalLM, GPT2Tokenizer

input_output_font = "System 16"
button_text_font = 'Courier 12'

model = None
tokenizer = None
outputs = ""
temp = 0.9
leng = 45


busy = False
#functions for buttons
def but_send_pressed():
    global busy
    global outputs
    print("Send button pressed")
    if busy == False:
        busy = True
        prefix = box_inp.get(1.0, "end-1c")
        outputs = outputs + prefix
        box_inp.delete(1.0, "end")
        prefix = ""
        prefix = outputs
        print("Input Prefix: " + prefix)
        outputs = generate_output(prefix)
        print(outputs)
        update_progress()
        busy = False
    else:
        print("Button already pressed, please wait.")

def but_clear_pressed():
    global outputs
    print("Clear button pressed")
    if messagebox.askyesno("Confirm Clear","Are you sure you want to clear output history?\nThis cannot be undone."):
        print("Confirmed clear")
        box_out.configure(state = "normal")
        box_out.delete(1.0, "end")
        box_out.configure(state = "disabled")
        outputs = ""

# this updates the output window
def update_progress():
    print("Updating output window...")
    print(outputs)
    box_out.configure(state = "normal")
    box_out.delete(1.0, "end")
    print(outputs)
    box_out.insert(END, outputs)
    box_out.configure(state = "disabled")
    print("Updated.")

# ai related functions for instancing or generating new outputs
def instance_model():
    global model
    global tokenizer
    print("Instancing GPT-NEO Small!")
    model_name = 'EleutherAI/gpt-neo-1.3B'
    model = GPTNeoForCausalLM.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    print("Done!")

def generate_output(prefix):
    print("Generating output!")
    input_ids = tokenizer(prefix, return_tensors="pt").input_ids
    leng = len(prefix) + 60
    gen_tokens = model.generate(input_ids, do_sample=True, temperature=temp, max_length=leng,)
    gen_text = tokenizer.batch_decode(gen_tokens)[0]
    print(gen_text)
    return gen_text

# used for the sliders to update temperature and length values
def update_temperature(new_temp):
    print("Slider adjusted...")
    global temp
    temp = float(new_temp)
    print(temp)

def update_length(new_leng):
    print("Slider adjusted...")
    global leng
    leng = new_leng
    print(leng)

# main window
main = tkinter.Tk()

main.wm_title("Tk Neo")
main.wm_resizable(False, False)
main.wm_minsize(1280,720)
main.wm_maxsize(1280,720)
main.configure(background="#111111")

# input box
box_inp_content=tkinter.StringVar(value = "")
box_inp = tkinter.Text(master = main)
box_inp.configure(background="#3B3B3B", foreground="white", font = input_output_font,width=120, height=3, border=5,insertbackground="white")
box_inp.place(x = 56, y = 550)

# output box
box_out_content=tkinter.StringVar()
box_out = tkinter.Text(master = main, font = input_output_font, width=128, height=24, border=5, background="black", foreground="white", state=DISABLED)
box_out.place(x = 56, y = 48)

# "send input" button
but_send = tkinter.Button(master = main)
but_send.configure(background = "grey", foreground = "white", font = "Arial 24", border = 4, height = 1, width = 3, text = ">", disabledforeground="black", command = but_send_pressed)
but_send.place(x = 1150, y = 553)

# "clear outputs" button
but_clear = tkinter.Button(master = main,background="grey",foreground = "white", border = 4, height = 1, width = 5, font = button_text_font, text = "Clear", command = but_clear_pressed)
but_clear.place(x = 56, y = 632)

# temperature slider
scl_temp_value = tkinter.DoubleVar
scl_temp = tkinter.Scale(master = main, from_ = 0.5, to = 3.0, label = "Temperature", variable = scl_temp_value, resolution = 0.1, troughcolor="grey", background="black", foreground="white", orient = HORIZONTAL, length = 150, font = button_text_font, command = update_temperature)
scl_temp.place (x = 128, y = 632)

# length slider
scl_leng_value = tkinter.IntVar
scl_leng = tkinter.Scale(master = main, from_ = 10, to = 800, label = "Length", variable = scl_leng_value, troughcolor="grey", background="black", foreground="white", orient = HORIZONTAL, length = 900, font = button_text_font, command = update_length)
scl_leng.place (x = 286, y = 632)

# just in case you're just testing UI based stuff and don't want the AI running too
valid_choice=False
while valid_choice == False:
    print("Instance NEO? Y/N")
    choice = input("> ")
    if choice.upper() == "Y":
        instance_model()
        valid_choice=True
    elif choice.upper() == "N":
        print("ok :(")
        valid_choice=True
    continue

# aaand go
main.mainloop()
