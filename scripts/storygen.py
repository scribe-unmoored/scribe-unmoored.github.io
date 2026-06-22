


# This code adds a short story link to the html of every other short story in "assorted corpora."

from pathlib import Path

directory = Path("writings/writings")

# MUST CHECK THESE BEFORE RUNNING!!!! ---------------------------------------------------

name = "test"         
html = "test.html"      	          
													                # KNOW BEFORE YOU WOE - Lucien Lachance

#----------------------------------------------------------------------------------------

# Define old <div class="sealed">*</div> placeholder.
# Define new chapter link.

placeholder = '<!-- placeholder -->'
new_link = f'<a class="published" href="{html}">{name}</a>'

replacement = placeholder + "\n" + new_link  # keep placeholder then indented link


# Search every file in directory.

for file in directory.rglob("*.html"):
    text = file.read_text(encoding="utf-8")

    if placeholder not in text:
        print(f"Missing placeholder in {file}")				# Useful for troubleshooting.
        continue

    text = text.replace(placeholder, replacement, 1)  # Replace only the first instance.

    file.write_text(text, encoding="utf-8")		  			# Readout showing updated files.
    print(f"Updated {file}")




