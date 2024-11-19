from django.shortcuts import render
import openai, os, requests
from dotenv import load_dotenv
from django.core.files.base import ContentFile
from images.models import Image

load_dotenv()

api_key = os.getenv("OPENAI_KEY", None)
openai.api_key = api_key

def generate_image_from_txt(request):
    if api_key is not None and request.method == "POST":
        user_input = request.POST.get('user_input')
        #prompt = f"if the text is related to food - answer it: {user_input}, else say: Sorry I can't show this"

        response = openai.Image.create(
            prompt = user_input,
            size = '256x256'
        )
        img_url = response["data"][0]["url"]

        response = requests.get(img_url)
        img_file = ContentFile(response.content)

        count = Image.objects.count() + 1
        fname = f"image-{count}.jpg"

        obj = Image(phrase=user_input)
        obj.ai_image.save(fname, img_file)
        obj.save()

        print(obj)

    return render(request, "mainImage.html", {})