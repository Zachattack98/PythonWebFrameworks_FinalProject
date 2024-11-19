from django.shortcuts import render
import openai, os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAPI_KEY")
openai.api_key = api_key

def questions_chatbot(request):
    chatbot_response = None
    if api_key is not None and request.method == 'POST':
        user_input = request.POST.get('user_input')
        #ensure that only questions pertaining to recipes are asked
        #prompt = f"if the question is related to recipes - answer it: {user_input}, else say: Sorry I can't answer this"
        prompt = user_input
        response = openai.Completion.create(
            engine = 'text-davinci-003',
            prompt = prompt,
            max_tokens = 100, #maximum of 100 characters for search bar
            temperature = 0.5
        )
        print(response)
    return render(request, 'mainChat.html', {})


