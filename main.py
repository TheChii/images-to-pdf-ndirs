import os
import shutil
from PIL import Image
from reportlab.pdfgen import canvas
from concurrent.futures import ThreadPoolExecutor

def pngs_to_pdf(directory):
    png_files = [f for f in os.listdir(directory) if f.endswith('.png')]
    if not png_files:
        return False  

    all_files = os.listdir(directory)
    if len(all_files) != len(png_files):
        return False 

    png_files.sort(reverse=True)  
    pdf_path = f"{directory}.pdf"
    c = canvas.Canvas(pdf_path)

    for png_file in png_files:
        img_path = os.path.join(directory, png_file)
        with Image.open(img_path) as img:  
            c.setPageSize(img.size)
            c.drawImage(img_path, 0, 0, width=img.size[0], height=img.size[1])
            c.showPage()

    c.save()

    try:
        shutil.rmtree(directory)
    except PermissionError:
        print(f"Could not delete the directory {directory} due to a PermissionError.")
    return True

def process_directory(dir_path):
    pngs_to_pdf(dir_path)

def process_directories(main_directory):
    directories = []
    for root, dirs, files in os.walk(main_directory, topdown=False):
        for name in dirs:
            dir_path = os.path.join(root, name)
            directories.append(dir_path)

    with ThreadPoolExecutor() as executor:
        executor.map(process_directory, directories)


main_directory = r"C:\Users\thech\Downloads\nt"    # folderul cu toate folderele cu imagini / alte foldere
process_directories(main_directory)
