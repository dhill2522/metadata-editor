import tkinter as tk
import datetime
from tkinter import filedialog
import subprocess
import shutil
import time

class App(object):
    def __init__(self):
        self.selectedFile = 'None Selected'

        self.g = tk.Tk()
        self.g.title('Simple Metadata Editor')

        self.btn_select = tk.Button(self.g, text='Select File', command=self.selectFile).grid(row=0, column=0)
        self.selectedFileLabel = tk.Label(self.g, text=self.selectedFile)
        self.selectedFileLabel.grid(row=0, column=1, columnspan=2)
        self.msg_label = tk.Label(self.g, text='')
        self.msg_label.grid(row=4, column=1, columnspan=2)

        tk.Label(self.g, text='(yyyy-mm-dd)').grid(row=1, column=1)
        tk.Label(self.g, text='(hh:mm:ss)').grid(row=1,   column=2)
        tk.Label(self.g, text='New date and time:').grid(row=2, column=0)

        self.new_date = tk.Entry(self.g)
        self.new_date.grid(row=2, column=1)
        self.new_time = tk.Entry(self.g)
        self.new_time.grid(row=2, column=2)


        self.btn_submit = tk.Button(self.g, text="Update Metabata", command=self.do_stuff).grid(row=5, column=1)
        self.btn_close = tk.Button(self.g, text="Close", command=self.g.destroy).grid(row=5, column=2)

        if not shutil.which('ffmpeg'):
            print('FFmpeg is not in the system path.')
            self.msg_label.config(text='Please install FFmpeg first. https://ffmpeg.org/')

    def selectFile(self):
        self.selectedFile = filedialog.askopenfilename(filetypes=(('MP4 video', '*.mp4'),))
        self.selectedFileLabel.config(text=self.selectedFile)

    def updateDate(self):
        # Run ffmpeg from commandline as the python package does not seem
        # to support updating metadata
        exit_code = subprocess.call(['ffmpeg', '-i', self.selectedFile, 
                                    '-metadata', f'creation_time={self.date.isoformat()}', 
                                    f'{self.selectedFile[:-4]}-updated.mp4'])
        if exit_code != 0:
            raise(Exception('Error updating metadata'))

    def do_stuff(self):
        time.sleep(0.1)
        self.msg_label.config(text='Updating metdata...')
        # Check to make sure the datetime is in the right format
        try:
            year, month, day = self.new_date.get().split('-')
            hour, minute, second = self.new_time.get().split(':')
            self.date = datetime.datetime(int(year), int(month), int(day), 
                                        int(hour), int(minute), int(second))

        except Exception as err:
            self.msg_label.config(text='Check your date and time format.')
            raise err

        # Update the metadata
        try:
            tk.Label(self.g, text='').grid(row=4, column=1, columnspan=2)
            self.updateDate()
        except Exception as err:
            self.msg_label.config(text='Error Updating metdata.')
            raise err

        self.msg_label.config(text='Metadata update successful..')

    def run(self):
        self.g.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
