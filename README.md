# HIIK-map
This is the interactive map of the Heidelberg Institute for International Conflict Research (HIIK). The HIIK is an independent and interdisplinary institute at the Department of Political Science at Heidelberg University. Since 1991, the HIIK is dedicated to the research, documentation and evaluation of intra-, inter-, trans- and sub-state political conflicts.

The Conflict Barometer is an annual analysis of global conflict events and the central publication of the HIIK. Non-violent and violent crises, wars, coups d'état as well as peace negotiations are the focus of the research. In the summary of the course of the conflicts taking place worldwide, the HIIK presents the developments of the respective year, which are explained graphically and in the form of texts. 

The contents include the following:
HIIK-map/
│
├── hiik-app/
│   ├── data/
│   │   ├── global.xlsx
│   │   ├── subnational.xlsx
│   │
│   ├── maps/
│   │   ├── global.json
│   │   ├── subnational.json
│   │
│   ├── scripts/
│   │   ├── global_map.py
│   │   ├── subnational_map.py
│   │
│   ├── main.py
│
├── Procfile
├── README.md
├── reguirements.txt
└── runtime.txt

Thus, the app is divided into two modules with two different maps. main.py is for combining those maps into one layout and displaying them. The maps are from gadm.org but edited since the HIIK uses different layers for some countries and the HASC-codes are different. Furthermore, the data files were originally provided by HIIK. I used Python to bring them into the necessary file structure.
