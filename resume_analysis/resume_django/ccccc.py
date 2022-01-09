import subprocess

file_path='我的简历.docx'
out_path='./opt'
# linux下将doc转化为pdf
subprocess.check_output(
    ["soffice", "--headless", "--invisible", "--convert-to", "pdf", file_path, "--outdir", out_path])