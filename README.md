# Mediapipe Python Static Image

A simple Python setup of MediaPipe - using the Static Image setting


Based on the [Mediapipe Python example][1] and [Google Colab Example][2]

# Getting Started

**Requirements**
- Python 3
- PIP3 (Comes along Python 3)

**Assets**
- Have an empty directory here `projectRoot/exports/images`
- Have your input images in `projectRoot/images`

**Steps**
After cloning/downloading/degitting etc.
1. In the root of the project, start an virtual environment  
`python3 -m venv mp_env && source mp_env/Scripts/activate`
2. Install the packages  
`pip install -r requirements.txt`
3. Run the script with
`python3 init.py`
4. `exports/output.json` and `exports/images` should now be populated
5. Enter `deactivate` to exit the virtual environment 


[1]: https://google.github.io/mediapipe/solutions/hands#python-solution-api
[2]: https://colab.research.google.com/drive/1FvH5eTiZqayZBOHZsFm-i7D-JvoB9DVz#scrollTo=BAivyQ_xOtFp