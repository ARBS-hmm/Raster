🎥 Computer Graphics Algorithms Visualization using Manim

This repository contains animated visualizations of fundamental Computer Graphics algorithms using Manim (Mathematical Animation Engine).
The project is designed to help students understand how classic raster graphics algorithms work step-by-step.

📌 Algorithms Implemented

✅ DDA Line Drawing Algorithm

✅ Bresenham Line Drawing Algorithm

✅ Midpoint Circle Drawing Algorithm

✅ Midpoint Ellipse Drawing Algorithm

Each algorithm is visualized clearly using animation to show pixel plotting and decision logic.

🛠️ Tech Stack

Python 3.10 / 3.11

Manim Community Edition

FFmpeg (for rendering videos)
```
 ## 📂 Project Structure
ComputerGraphics/
│
├── Raster/
│ ├── dda.py
│ ├── bresenham.py
│ ├── midpoint_circle.py
│ ├── midpoint_ellipse.py
│
├── .gitignore
├── README.md
```

⚠️ Rendered videos are excluded using .gitignore to keep the repository clean.

⚙️ Installation Guide
1️⃣ Clone the repository
https://github.com/ARBS-hmm/Raster.git
cd computer-graphics-manim

2️⃣ Create and activate virtual environment
python -m venv manim-env
manim-env\Scripts\activate

3️⃣ Install Manim
pip install manim

4️⃣ Verify installation
manim --version

▶️ How to Run Animations
▶️ DDA Line Algorithm
manim -pql dda.py DDALine

▶️ Bresenham Line Algorithm
manim -pql bresenham.py BresenhamLine

▶️ Midpoint Circle Algorithm
manim -pql midpoint_circle.py MidPointCircle

▶️ Midpoint Ellipse Algorithm
manim -pql midpoint_ellipse.py MidPointEllipse


-pql → preview + low quality (fast rendering)

🎯 Learning Objectives

Understand rasterization algorithms visually

Learn how decision parameters work in line & curve drawing

Bridge theory (exam) with visual intuition

Explore Manim for algorithm animation

📸 Sample Output

Smooth line drawing using integer arithmetic

Symmetric plotting in circles and ellipses

Step-by-step visualization of pixel selection

(Videos are generated locally and not pushed to GitHub)

🧠 Academic Relevance

This project is highly useful for:

Computer Graphics (3rd Semester)

Viva & practical exams

Algorithm visualization

Teaching and demonstrations

🤝 Contributing

Contributions are welcome!
Feel free to:

Improve animations

Add comments for clarity

Add new CG algorithms

📜 License

This project is for educational purposes.

⭐ Acknowledgements
Manim Community
Computer Graphics textbooks & syllabus
Manim Community

Computer Graphics textbooks & syllabus
