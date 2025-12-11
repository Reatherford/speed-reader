🏃 SpeedRead — A Python Rapid Serial Visual Presentation (RSVP) Reader

SpeedRead is a fast, customizable PDF speed-reading application written in Python using Tkinter.

It displays one word at a time (RSVP-style) and includes advanced features similar to Spritz:

🌗 Dark & Light Mode

🎨 Custom Text Color + Custom Focus Letter Color

⏯ Pause / Resume (no losing your position)

🔤 Focus Letter Highlighting (on/off)

🎯 Optimal Recognition Point (ORP) Alignment (on/off)

🧠 Sentence-Aware Timing (on/off; extra pause at punctuation)

📍 Start reading from any percentage (%) into the document

📄 Extracts and reads text from PDF files using PyPDF2

This README is intentionally written for complete beginners on Ubuntu, macOS, and Windows.

📦 Requirements (All Platforms)

SpeedRead requires:

Python 3.10+

Tkinter

PyPDF2

That’s ALL.

🐧 Ubuntu / Linux Installation (Beginner Friendly)
1. Install Python + Tkinter + Virtual Environment Support
sudo apt update
sudo apt install -y python3 python3-tk python3-venv

2. Clone this repository
cd ~/Desktop
git clone https://github.com/Reatherford/speed-reader.git
cd speed-reader

3. Create & Activate Virtual Environment
python3 -m venv venv
source venv/bin/activate

4. Install Required Python Package
pip install PyPDF2

5. Run the Program
python speedRead.py

🍎 macOS Installation (Beginner Friendly)
1. Install Python 3

Install Homebrew (if needed):

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"


Install Python:

brew install python


Tkinter comes bundled with the macOS Python installer.

2. Clone the repository
git clone https://github.com/Reatherford/speed-reader.git
cd speed-reader

3. Create & Activate Virtual Environment
python3 -m venv venv
source venv/bin/activate

4. Install PyPDF2
pip install PyPDF2

5. Run the Program
python speedRead.py

🪟 Windows Installation (Beginner Friendly)
1. Install Python

Download here:
https://www.python.org/downloads/

IMPORTANT:
During installation, CHECK THE BOX:

✔ Add Python to PATH

Tkinter is included automatically.

2. Clone the Repository

Install Git:
https://git-scm.com/download/win

Then in Command Prompt:

cd %USERPROFILE%\Desktop
git clone https://github.com/Reatherford/speed-reader.git
cd speed-reader

3. Create & Activate Virtual Environment
python -m venv venv
venv\Scripts\activate

4. Install PyPDF2
pip install PyPDF2

5. Run the App
python speedRead.py

📄 requirements.txt

Because your app uses only one pip dependency, your requirements file should contain:

PyPDF2


Tkinter is system-installed on Linux and bundled with Python on macOS/Windows.

▶️ How to Use the App

Click Load PDF and choose any text-based PDF.

Choose Dark Mode or Light Mode.

Pick text color and focus-letter color (optional).

Adjust the WPM slider (words per minute).

Move the Start Position slider to jump to any % of the document.

Toggle features ON/OFF:

Focus Letter

ORP Alignment

Sentence-Aware Timing

Click Start to begin reading.

Click Pause to pause, click again to Resume.

🔤 What Is a Focus Letter?

Every word has one character that your eyes naturally fixate on to recognize the word most efficiently.

The app highlights this character (in red by default) to:

reduce eye movement

increase recognition speed

stabilize your visual anchor

You can turn this feature on/off.

🎯 What Is ORP (Optimal Recognition Point)?

The Optimal Recognition Point is the letter position in a word that:

your brain processes fastest

your eye naturally falls on

greatly reduces reading fatigue

For example, in the word “reading”:

rea[d]ing
     ^


The ORP (“d”) stays aligned in the same screen location for every word.
This removes the need for your eyes to move side-to-side.

You can toggle ORP alignment ON or OFF.

🧠 Sentence-Aware Timing

If enabled:

Commas / semicolons → slightly longer pause

Periods / question marks → double pause

This makes RSVP feel more natural and improves comprehension.

🛠 How It Works (Technical Overview)

PDF text is extracted using PyPDF2

Text is cleaned and split into individual words

Words are displayed on a Tkinter Canvas

ORP index is calculated using a heuristic (~35% into the word)

The ORP character is:

Highlighted (optional)

Center-aligned (optional)

A timed loop displays each word based on:

Your WPM setting

Sentence-aware timing rules

Pause/Resume controls the reading loop without losing your place

❗ Troubleshooting Guide
✔ “ModuleNotFoundError: No module named 'tkinter'” (Ubuntu)

Install Tkinter:

sudo apt install python3-tk

✔ “ModuleNotFoundError: No module named 'PyPDF2'”

Your venv is not active or PyPDF2 is not installed:

source venv/bin/activate
pip install PyPDF2

✔ PDF shows blank text

Your PDF is likely scanned images, not real text.
Use OCR:

sudo apt install tesseract-ocr

✔ Nothing happens when launching

Ensure you run inside your venv:

source venv/bin/activate
python speedRead.py

🤝 Contributions

Feature requests and pull requests are welcome.

Good candidates:

Word progress indicator

Multiple-word display mode

Save reading position

Adjustable ORP algorithms

UI theme packs

📜 License

MIT License
You can use, modify, distribute, and build upon this software freely.
