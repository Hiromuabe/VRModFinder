import openai
import os
import re

def gpt_interior(input_text):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt1 = "You are a space designer. "
    prompt2 = "Output three types of interior from the following space concept."
    prompt_input = "Space Concept: " + input_text
    prompt3 = "And the name of the interior should be simple and singular form, like table and desk."
    prompt_not = "Don't output room name like library or kitchen."
    prompt4 = "Output only types of interior like chair and bookshelf."
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
                {"role": "system", "content": prompt1+prompt2},
                {"role": "user", "content": prompt_input},
                {"role":"system","content":prompt3},
                {"role":"system","content":prompt_not},
                {"role":"system","content":prompt4},
                ]
    )
    interior = response["choices"][0]["message"]["content"]
    pattern = r'\d+\.\s'  # 正規表現パターン：数字とピリオドの後に空白が続く部分を検索
    interior_list = [j.lower() for j in [re.sub(pattern,"",i) for i in interior.split("\n")]]
    return interior_list

def gpt_feature(input_text, interior_name):
    prompt5 = "You are a space designer. "
    prompt6 = f"Please output the characteristics of {interior_name} from the following space concept."
    prompt_input = "Space Concept: " + input_text
    prompt7 = "Please express very short their characteristics in terms of color, size, and texture like yellow and leather."
    prompt8 = "Please output only characteristics like desk:white and leather."
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
                {"role": "system", "content": prompt5+prompt6},
                {"role": "user", "content": prompt_input},
                {"role":"system","content":prompt7},
                {"role":"system","content":prompt8},
                ]
    )
    features = response["choices"][0]["message"]["content"]
    pattern2 = r'^[^:]*:\s*'  # 正規表現パターン：コロンより前の部分を検索
    features_list = [re.sub(pattern2,"",i) for i in features.split("\n")]
    return features_list

def gpt_number(input_text,interior_name):
    prompt9 = "You are a space designer. "
    prompt10 = f"Please output the number of {interior_name} from the following space concept."
    prompt_input = "Space Concept: " + input_text
    prompt11 = "Please output only number like 'desk:2'."

    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
                {"role": "system", "content": prompt9+prompt10},
                {"role": "user", "content": prompt_input},
                {"role":"system","content":prompt11},
                ]
    )
    num = response["choices"][0]["message"]["content"]
    # pattern2 = r'^[^:]*:\s*'  # 正規表現パターン：コロンより前の部分を検索
    # num_list = [int(re.sub(pattern2,"",i)) for i in num.split(",")]
    return num
