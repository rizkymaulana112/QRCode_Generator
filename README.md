# QRCode_Generator
During my internship at PT Phapros Tbk, I assisted the EHS (Environment, Health, and Safety) division by developing an automated QR Code generation system. This system eliminated the need to create QR Codes manually one by one, making the process faster and more efficient.

# Features
- Impoert an data from excel
- Add Logo of division company
- Simple dekstop interface using PySide6
- Unic sound will appear when the generate is done
- Create hyperlinks to MS Form or Google Form (universal)
- Export result to excel and folder thats contains QR code
- Generate QR Codes automatically

# How to  make Python to .exe
1. Install PyInstaller = pip install pyinstaller
2. Navigate to the project directory = cd D:\QR_APAR
3. Build the executable = pyinstaller -w app.py
4. Wait for the build process to finish 
dist/
5. Location =
dist/
└── app/
    └── app.exe
6. Before running the application, copy  the following/files into the same directory as app.exe
dist/
└── app/
    ├── app.exe
    ├── sound/
    ├── gambar/
    └── logo_ehs.png
    
# How to Use
1. Open folder dist, go to folder app, and run app.exe
2. Choose excel file thats contain datasheet (No, Kode, Ruangan)
3. Choose logo that want to use
4. Choose where folder of result will you given
5. Name file output (excel)
6. Paste the base URL from MS Form or Google Form
7. For example: https://docs.google.com/forms/d/e/1FAIpQLSdA3cAJZyXng-oERAYxP757_DSz-iGm276O2QNxmeLV8CBK-g/viewform?usp=pp_url&entry.839337160=TTSK-1&entry.1750026248=Gd J Lantai 1
8. remove to this: https://docs.google.com/forms/d/e/1FAIpQLSdA3cAJZyXng-oERAYxP757_DSz-iGm276O2QNxmeLV8CBK-g/viewform?usp=pp_url&entry.839337160={Kode}&entry.1750026248={Ruangan}
9. Generate, if it was generated, the unic sound will be play once

# Author
Rizky Maulana Hendradi
Thanks for your attention
