

# This code reads through every html file in a episode and replaces the placeholder there with a new link and (optionally) a new placeholder after that link.


from pathlib import Path

#Translate dictionary so placeholders show up in Daedric font.

number_translate = {
	1: "one",
	2: "two",
	3: "three",
	4: "four",
	5: "five",
	6: "six",
	7: "seven",
	8: "eight",
	9: "nine",
	10: "ten",
	11: "eleven",
	12: "twelve",
	13: "thirteen",
	14: "fourteen",
	15: "fifteen",
	16: "sixteen",
	17: "seventeen",
	18: "eighteen",
	19: "nineteen",
	20: "twenty",
	21: "twenty one",
	22: "twenty two",
	23: "twenty three",
	24: "twenty four",
	25: "twenty five",
	26: "twety six",
	27: "twenty seven",
	28: "twenty eight",
	29: "twenty nine",
	30: "thirty",
	31: "thirty one",
	32: "thirty two",
	33: "thirty three",
	34: "thirty four",
	35: "thirty five",
	36: "thirty six",
	37: "thirty seven",
	38: "thirty eight",
	39: "thirty nine",
	40: "forty",
	41: "forty one",
	42: "forty two",
	43: "forty three",
	44: "forty four",
	45: "forty five",
	46: "forty six",
	47: "forty seven",
	48: "forty eight",
	49: "forty nine",
	50: "fifty"
}



# MUST CHECK THESE BEFORE RUNNING!!!! ---------------------------------------------------
													#									|
directory = Path("adventures/brasstower")			# DO YOU HAVE THE RIGHT EPISODE?  	|
chapter = 11										# DO YOU HAVE THE RIGHT CHAPTER?  	|
add_sealed_placeholders = True						# DO YOU WANT A PLACEHOLDER AFTER?	|
													# KNOW BEFORE YOU WOE				|
#----------------------------------------------------------------------------------------

# Define old <div class="sealed">*</div> placeholder.
# Define new chapter link.

old_placeholder = f'<div class="sealed">Chapter {number_translate[chapter]}</div>'
new_link = f'<a class="published" href="chapter{chapter}">Chapter {chapter}</a>'


# Determine what to do if add_sealed_placeholders is True or False.

if add_sealed_placeholders:
    new_placeholder = f'        <div class="sealed">Chapter {number_translate[chapter + 1]}</div>'
    replacement = new_link + "\n" + new_placeholder  # Add new chapter, one newline, then new placeholder.
else:
    replacement = new_link  # OR only add new chapter. Useful towards the end.


# Search every file in episode directory.

for file in directory.rglob("*.html"):
    text = file.read_text(encoding="utf-8")

    if old_placeholder not in text:
        print(f"Missing placeholder in {file}")				# Useful for troubleshooting.
        continue

    text = text.replace(old_placeholder, replacement, 1)	# Replace old with new; does this for only the first occurence in each file.

    file.write_text(text, encoding="utf-8")					# Readout showing updated files.
    print(f"Updated {file}")

