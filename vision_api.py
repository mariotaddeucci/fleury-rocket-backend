import requests


def read_image_text(image_path):
    subscription_key = "53d24d7d8c474730bb804f945196e725"

    vision_base_url = "https://brazilsouth.api.cognitive.microsoft.com/vision/v2.0/"
    analyze_url = vision_base_url + "ocr"

    # image_data = open(image_path, "rb").read()
    image_data = requests.get(image_path, stream=True)
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()
    analysis = response.json()

    texts = []
    for region in analysis['regions']:
        for line in region['lines']:
            for word in line['words']:
                text = word['text'].upper().strip('.').strip(';')
                texts.append(text)

    return texts
