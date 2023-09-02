import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
input_text = input("空間コンセプト:")
prompt = "以下の日本語を英語にしてください。"

prompt1 = "You are a space designer. "
prompt2 = "Output three types of interior from the following space concept."
prompt_input = "Space Concept: "
prompt3 = "And the name of the interior should be simple and singular form, like table and desk."
prompt_not = "Don't output room name like library or kitchen."
prompt4 = "Output only types of interior like chair and bookshelf."
openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
model="gpt-4",
messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_text},
            {"role":"system","content":"ただし結果のみ返信してください。"}
            ]
)

en_text = response["choices"][0]["message"]["content"]
print(en_text)

response = openai.ChatCompletion.create(
model="gpt-4",
messages=[
            {"role": "system", "content": prompt1+prompt2},
            {"role": "user", "content": prompt_input},
            {"role":"system","content":prompt3+en_text},
            {"role":"system","content":prompt_not},
            {"role":"system","content":prompt4},
            ]
)
interior = response["choices"][0]["message"]["content"]

response = openai.ChatCompletion.create(
model="gpt-4",
messages=[
            {"role": "system", "content": "以下の英文をわかりやすい日本語に和訳してください"},
            {"role": "user", "content": interior},
            {"role":"system","content":"ただし結果のみ返信してください。"}
            ]
)

ja_text = response["choices"][0]["message"]["content"]
print(ja_text)