# import google.generativeai as genai

# genai.configure(api_key="GOOGLE_API_KEY"")

# # model = genai.GenerativeModel("gemini-1.5-flash")

# for model in genai.list_models():
#     print(model.name)

import google.generativeai as genai

genai.configure(api_key="GOOGLE_API_KEY")

model = genai.GenerativeModel("models/gemini-2.5-flash")

response = model.generate_content("What is coding?")
print(response.text)







# pip install openai 
# if you saved the key under a different environment variable name, you can do something like: 
# client = OpenAI(
#     api_key="Open_AI_Key",
# ) 

# completion = client.chat.completions.create(
#     model="gpt-5-nano",
#     messages = [
#     {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
#     {"role": "user","content": "what is coding?"}
    
#   ]
# )

# print(completion.choices[0].message)
