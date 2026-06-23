


# This code adds a short story link to the html of every other short story in "assorted corpora."

from pathlib import Path

directory = Path("writings/writings")

# MUST CHECK THESE BEFORE RUNNING!!!! ---------------------------------------------------

name = "He Can"         
html = "he-can.html"      	   
       
# KNOW BEFORE YOU WOE - Lucien Lachance

#----------------------------------------------------------------------------------------

placeholder = '<!-- placeholder -->'
new_link = f'               <a class="published" href="{html}">{name}</a>'

replacement = placeholder + "\n" + new_link                 # keep placeholder then indented link


# Search every file in directory.

for file in directory.rglob("*.html"):                      # .rglob searches recursively for all .html files in the directory and its subdirectories.
    text = file.read_text(encoding="utf-8")                 # file.read_text reads the content of the file with UTF-8 encoding to handle special characters properly.

    if placeholder not in text:
        print(f"Missing placeholder in {file}")				# Useful for troubleshooting, in case the placeholder is missing.
        continue

    text = text.replace(placeholder, replacement, 1)        # text.replace replaces the first occurrence of the placeholder with the new link, ensuring that only one replacement is made per file.

    file.write_text(text, encoding="utf-8")		  			# Readout showing updated files. UTF-8 encoding is used to ensure proper handling of special characters.
    print(f"Updated {file}")




