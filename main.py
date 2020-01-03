import tkinter as tk
import datetime
from tkinter import filedialog
import subprocess

def selectFile():
    f = filedialog.askopenfilename()
    print('Selected File:', f)
    if f:
        selectedFileLabel.config(text=f)

def updateDate(date):
    # Run ffmpeg from commandline as the python package does not seem
    # to support updating metadata
    tk.Label(g, text='Updating metdata...').grid(row=4, column=1, columnspan=2)
    d = f"{date['y']}-{date['mo']}-{date['d']}T{date['h']}:{date['mi']}:{date['s']}"
    selectedFile = selectedFileLabel.cget('text')
    print(['ffmpeg', '-i', selectedFile, '-metadata', f'creation_time={d}', f'{selectedFile[:-4]}-updated.mp4'])
    exit_code = subprocess.call(['ffmpeg', '-i', selectedFile, 
                                '-metadata', f'creation_time={d}', f'{selectedFile[:-4]}-updated.mp4'])
    if exit_code != 0:
        raise(Exception('Error updating metadata'))

def do_stuff():
    # Check to make sure the datetime is in the right format
    try:
        year, month, day = new_date.get().split('-')
        hour, minute, second = new_time.get().split(':')

        new_datetime = {
            'y': int(year),
            'mo': int(month),
            'd': int(day),
            'h': int(hour),
            'mi': int(minute),
            's': int(second)
        }

        # new_datetime = datetime.datetime(int(year), int(month), int(day), 
                                            # int(hour), int(minute), int(second))
        # print('new datetime:', new_datetime.isoformat())
    except Exception as err:
        tk.Label(g, text='Check your date and time format.').grid(row=4, column=1, columnspan=2)
        raise err

    try:
        updateDate(new_datetime)
    except Exception as err:
        tk.Label(g, text='Error updating metadata.').grid(row=4, column=1, columnspan=2)
        raise err

    tk.Label(g, text='Metadata update successful.').grid(row=4, column=1, columnspan=2)

g = tk.Tk()
g.title('Simple Metadata Editor')

# FIXME: use shutil to check if ffmpeg exists and set label if not.

btn_select = tk.Button(g, text='Select File', command=selectFile).grid(row=0, column=0)
selectedFileLabel = tk.Label(g, text='None Selected')
selectedFileLabel.grid(row=0, column=1, columnspan=2)

tk.Label(g, text='(yyyy-mm-dd)').grid(row=1, column=1)
tk.Label(g, text='(hh:mm:ss)').grid(row=1,   column=2)

tk.Label(g, text='New date and time:').grid(row=2, column=0)
new_date = tk.Entry(g)
new_date.grid(row=2, column=1)
new_time = tk.Entry(g)
new_time.grid(row=2, column=2)

btn_submit = tk.Button(g, text="Update Metabata", command=do_stuff).grid(row=5, column=1)
btn_close = tk.Button(g, text="Close", command=g.destroy).grid(row=5, column=2)

g.mainloop()
