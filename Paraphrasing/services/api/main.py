import os
import openai
from decouple import config


class client_request:
  
  def __init__(self):
    openai.api_key = config('API_KEY')
    
  def multi_function(self, text):
    prompt_text = text

    response = openai.Completion.create(
      engine="gpt-3.5-turbo",
      prompt=prompt_text,
      temperature=0.7,
      max_tokens=1000,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    x = response['choices']
    return (x[0]['text'])
