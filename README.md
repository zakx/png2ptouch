png2ptouch
==========

A Python script that reads PNG files and prints them on a Brother P2430PC.
It has been verified to print on 12mm and 24mm tape correctly.

Usage
=====
1. Set up your Brother P-Touch 2430PC in CUPS (maybe via the web UI, http://localhost:631/). You may use the foomatic ptouch driver or, if it's not available, the Generic Line printer profile will be okay, too.
2. Create a PNG file that is either 64px (for both 9mm/0.35" and 12mm/0.47" tape) or 128px (for 24mm/0.94" tape) tall.
3. `pip install -e .`
4. Run `printpng -p CUPS_Printer_Name image.png` to print.

You may extract the exact printer name by running `lpstat -a`.
