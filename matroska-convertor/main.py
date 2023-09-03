import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import subprocess
import os
import re
import threading

def update_progress(progress_bar, mp4_file_path):
    duration = 0
    process = subprocess.Popen(
        ['ffmpeg', '-i', mp4_file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stderr.decode('utf-8'), re.DOTALL).groupdict()
    
    if matches:
        duration = float(matches['hours'])*3600 + float(matches['minutes'])*60 + float(matches['seconds'])
    
    if duration == 0:
        print("Could not determine video duration.")
        return

    process = subprocess.Popen(
        ['ffmpeg', '-i', mp4_file_path, '-codec', 'copy', '-y', 'output.mp4'],
        stderr=subprocess.PIPE,
    )

    regex = re.compile(r"time=(\d+:\d+:\d+\.\d+)")

    while True:
        line = process.stderr.readline().decode('utf-8')
        if line == '' and process.poll() is not None:
            break

        match = regex.search(line)
        if match:
            time_str = match.group(1)
            hours, minutes, seconds = map(float, re.split('[:.]', time_str))
            elapsed_time = hours * 3600 + minutes * 60 + seconds
            progress = (elapsed_time / duration) * 100
            progress_bar['value'] = progress

def convert_mkv_to_mp4(mkv_file_path, progress_bar):
    mp4_file_path = os.path.splitext(mkv_file_path)[0] + '.mp4'
    
    # Start a separate thread to update the progress bar
    threading.Thread(target=update_progress, args=(progress_bar, mkv_file_path)).start()
    
    command = [
        'ffmpeg',
        '-i', mkv_file_path,
        '-codec', 'copy',
        mp4_file_path
    ]
    
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Conversion completed: {mkv_file_path} to {mp4_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def open_file_dialog(progress_bar):
    file_path = filedialog.askopenfilename(title = "Select MKV file", filetypes = [("MKV files","*.mkv")])
    
    if not file_path:
        return
    
    convert_mkv_to_mp4(file_path, progress_bar)

root = tk.Tk()
root.title("MKV to MP4 Converter")

progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate', maximum=100)
progress_bar.pack(fill=tk.X)

openButton = tk.Button(root, text = "Open MKV File", command = lambda: open_file_dialog(progress_bar))
openButton.pack()

root.mainloop()
