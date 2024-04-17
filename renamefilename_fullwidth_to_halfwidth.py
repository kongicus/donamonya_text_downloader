import os


def fullwidth_to_halfwidth(text):
    halfwidth_text = ''
    for char in text:
        if '０' <= char <= '９':
            halfwidth_text += chr(ord(char) - 0xFEE0)
        elif char in ['（', '）', '～']:
            halfwidth_text += chr(ord(char) - 0xFEE0)
        else:
            halfwidth_text += char
    return halfwidth_text


def rename_files(path):
    for filename in os.listdir(path):
        full_path = os.path.join(path, filename)
        if os.path.isfile(full_path):
            file_name, file_ext = os.path.splitext(filename)
            new_file_name = fullwidth_to_halfwidth(file_name)
            if new_file_name != file_name:
                new_full_path = os.path.join(path, new_file_name + file_ext)
                os.rename(full_path, new_full_path)


path = "doya_text_download"
rename_files(path)