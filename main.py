from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import threading
import time
import sys


class Typing:
    def __init__(self):
        # Instantiation
        self.text = ''
        self.typing_speed = 0
        self.no_lines = 0
        self.no_chars = 0
        self.word_count = 0
        self.thread = None
        self.thread_state = False
        self.count = 0

        ''' Root Window'''
        self.root = Tk()
        self.root.title("Typing Test ....")
        self.root.geometry('820x465+250+200')

        ''' Close Option '''
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)

        ''' Frame 0'''
        self.frame = ttk.LabelFrame(self.root, text=' Typing Area ', borderwidth=5)
        self.frame.pack(side=LEFT, expand=True, fill=BOTH, padx=10, pady=10)
        self.text_area = Text(self.frame, background='light blue', font=('Courier', 15), width=50, height=20)
        self.vertical_scroll = Scrollbar(self.frame, orient='vertical', command=self.text_area.yview)
        self.vertical_scroll.pack(side=RIGHT, fill='y')
        self.text_area.configure(state=DISABLED, yscrollcommand=self.vertical_scroll.set)
        self.text_area.bind('<BackSpace>', lambda _: 'break')
        self.text_area.pack(padx=5, pady=5, expand=True, fill=BOTH)

        ''' Frame 1 '''
        self.frame1 = ttk.LabelFrame(self.root, text=' Timer ')
        self.frame1.pack(side=TOP, expand=True, fill=X, padx=10, pady=10)

        self.counter = Label(self.frame1, text=str(self.count), fg='red', font=('arial', 30))
        self.counter.pack(padx=5, expand=True, fill=BOTH)

        ''' Frame 2 '''
        self.frame2 = ttk.LabelFrame(self.root, text=' Statistics ')
        self.frame2.pack(side=TOP, expand=True, fill=X, padx=10, pady=10)

        self.word_count_label = ttk.Label(self.frame2, text='No.of words : ')
        self.word_count_label.grid(row=0, column=0, pady=5, padx=10)
        self.word_count_res = ttk.Label(self.frame2, text=self.word_count)
        self.word_count_res.grid(row=0, column=1, pady=5, padx=10)

        self.no_chars_label = ttk.Label(self.frame2, text='No.of Chars  : ')
        self.no_chars_label.grid(row=1, column=0, pady=5, padx=10)
        self.no_chars_res = ttk.Label(self.frame2, text=self.no_chars)
        self.no_chars_res.grid(row=1, column=1, pady=5, padx=10)

        self.no_lines_label = ttk.Label(self.frame2, text='No.of Lines   : ')
        self.no_lines_label.grid(row=2, column=0, pady=5, padx=10)
        self.no_lines_res = ttk.Label(self.frame2, text=self.no_lines)
        self.no_lines_res.grid(row=2, column=1, pady=5, padx=10)

        self.words_speed_label = ttk.Label(self.frame2, text='Words / min : ')
        self.words_speed_label.grid(row=3, column=0, pady=5, padx=10)
        self.words_speed_res = ttk.Label(self.frame2, text=self.typing_speed)
        self.words_speed_res.grid(row=3, column=1, pady=5, padx=10)

        self.refresh_button = ttk.Button(self.frame2, text='Refresh', command=self.refresh_button_action,
                                         state=DISABLED)
        self.refresh_button.grid(row=4, columnspan=2, pady=5, padx=10)

        ''' Frame 3 '''
        self.frame3 = ttk.LabelFrame(self.root, text=' Controls ')
        self.frame3.pack(side=TOP, expand=True, fill=X, padx=10, pady=10)

        self.start_button = ttk.Button(self.frame3, text='Start', command=self.start_button_action)
        self.start_button.pack(pady=5, padx=10)

        self.stop_button = ttk.Button(self.frame3, text='Stop', state=DISABLED, command=self.stop_button_action)
        self.stop_button.pack(pady=5, padx=10)

        self.reset_button = ttk.Button(self.frame3, text='Reset', command=self.reset_button_action, state=DISABLED)
        self.reset_button.pack(pady=5, padx=10)

        self.exit_button = ttk.Button(self.frame3, text='EXIT', command=self.close_program)
        self.exit_button.pack(pady=7, padx=10)

        ''' Frame 4 (Ignore this frame) '''
        self.frame4 = Frame(self.root)
        self.frame4.pack(side=RIGHT, fill=BOTH, pady=5000)

        ''' Loop '''
        self.root.mainloop()

    def refresh_button_action(self):
        self.text = self.text_area.get('1.0', 'end')

        ''' Word Count '''
        if self.text.count(' ') == 0:
            self.word_count = 0
        else:
            self.word_count = self.text.count(' ') + 1
        self.word_count_res.configure(text=str(self.word_count))

        ''' Chars Count'''
        self.no_chars = len(self.text) - self.text.count('\n')
        self.no_chars_res.configure(text=str(self.no_chars))

        ''' Lines Count'''
        if self.no_chars == 0 and self.text.count('\n') == 1:
            self.no_lines = 0
        else:
            self.no_lines = self.text.count('\n')
        self.no_lines_res.configure(text=str(self.no_lines))

        ''' Words per minute'''
        self.typing_speed = self.word_count // (self.count / 60)
        self.words_speed_res.configure(text=str(self.typing_speed))

    def start_button_action(self):
        self.start_button.configure(state=DISABLED)
        self.stop_button.configure(state=NORMAL)
        self.text_area.configure(state=NORMAL)
        self.reset_button.configure(state=NORMAL)
        self.refresh_button.configure(state=NORMAL)

        ''' Thread '''
        self.thread_state = False
        self.thread = threading.Thread(target=self.increment_counter)
        self.thread.start()

    def increment_counter(self):
        while self.thread_state is False:
            self.count += 1
            self.counter.configure(fg='red', text=str(self.count - 1))
            time.sleep(1)

    def stop_button_action(self):
        self.stop_button.configure(state=DISABLED)
        self.start_button.configure(state=NORMAL)
        self.text_area.configure(state=DISABLED)
        self.thread_state = True

    def reset_button_action(self):
        self.text_area.configure(state=NORMAL)
        self.text_area.delete('1.0', 'end')
        self.text_area.configure(state=DISABLED)
        self.refresh_button_action()
        self.refresh_button.configure(state=DISABLED)
        self.stop_button.configure(state=DISABLED)
        self.start_button.configure(state=NORMAL)
        self.reset_button.configure(state=DISABLED)
        self.counter.configure(fg='red', text='0')
        self.thread_state = True
        self.count = 0

    def close_program(self):
        response = messagebox.askyesno(title='EXIT', message='Do you want to EXIT??')
        if response:
            self.thread_state = True
            sys.exit()


if __name__ == '__main__':
    typing_obj: Typing = Typing()
