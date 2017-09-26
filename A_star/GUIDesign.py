from tkinter import *
from A_Star import *

state = 2
obstacles = []
start = ""
end = ""
btn_dict = {}


def button_click(id):
    global state, start, end, btn_dict, obstacles
    if state == -1:
        return
    elif state == 1:
        btn = btn_dict[id]
        btn.configure(highlightbackground='red')
        if id not in obstacles:
            obstacles.append(id)
    elif state == 2:
        if len(start) != 0:
            former_btn = btn_dict[start]
            former_btn.configure(highlightbackground='white')
        cur_btn = btn_dict[id]
        cur_btn.configure(highlightbackground='green')
        start = id
    else:
        if len(end) != 0:
            former_btn = btn_dict[end]
            former_btn.configure(highlightbackground='white')
        cur_btn = btn_dict[id]
        cur_btn.configure(highlightbackground='yellow')
        end = id


def clear():
    global btn_dict
    if len(btn_dict) != 0:
        for btn in btn_dict.values():
            btn.configure(highlightbackground='white')


def m_radio(ctl):
    global state
    state = ctl.get()


def m_calcul():
    global state, start, end, btn_dict, obstacles
    algo = A_Star(start=start, end=end, obstacles=obstacles)
    path = algo.get_path()
    if len(path) > 0:
        for id in path:
            if id != start and id != end:
                btn = btn_dict[id]
                btn.configure(highlightbackground='black')


if __name__ == "__main__":
    root = Tk()
    root.title("A star")
    root.geometry("600x400+100+200")
    frame0 = Frame(root, height=5)
    frame0.grid(row=0)
    label = Label(frame0, text="A star alogrithm", width=65, bg="green")
    label.grid(row=0)
    frame1 = Frame(root)
    frame1.grid(row=1)
    btn_dict = {}
    for i in range(10):
        for j in range(20):
            m_text = "[%d,%d]" % (i, j)
            btn_text = StringVar()
            # btn_text.set(m_text)
            button = Button(frame1, textvariable=btn_text, borderwidth=5)
            btn_id = m_text
            button.configure(command=lambda id=btn_id: button_click(id))
            button.grid(row=i, column=j)
            btn_dict[m_text] = button
    foo = IntVar()
    count = 0
    frame3 = Frame(root)
    frame3.grid(row=2)
    for m_text, value in [('obstacle', 1), ('start', 2), ('end', 3)]:
        # m_value = IntVar()
        # m_value.set(value)
        r = Radiobutton(frame3, text=m_text, value=value, variable=foo)
        r.configure(command=lambda ctl=foo: m_radio(ctl))
        r.grid(row=0, column=10 + count)
        count += 1
    foo.set(2)

    frame4 = Frame(root)
    frame4.grid(row=3)
    button = Button(frame4, text="clear")
    button.configure(command=clear)
    button.grid()

    frame5 = Frame(root)
    frame5.grid(row=4)
    button = Button(frame5, text="calculate")
    button.configure(command=m_calcul)
    button.grid()
    root.mainloop()
