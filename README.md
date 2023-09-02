# VRModFinder

### how to use
1. Download a file from https://drive.google.com/drive/folders/1PncnUg75SLjnPWGMMkG9MM_dGAbCLc7R?usp=sharing
2. Make environment
   ```
   python -m venv (name)
   source (name)/bin/activate
   pip install --upgrade pip && pip install -r requirements.txt
   ```
3. Change path for json file in clip_code.py, line 65.
4. Change path for OpenAI API in gpt.py, line 6.
5. If you'd like to use its Eng ver,
   ```python index_en.py```
   If you'd like to use its Japanese ver,
   ```python index_ja.py```
