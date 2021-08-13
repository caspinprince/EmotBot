import requests

emoji = {'joy': ':smile:',
            'sadness': ':cry:',
            'anger': ':angry:',
            'fear': ':cold_sweat:',
            'love': ':smiling_face_with_3_hearts:',
            'surprise': ':astonished:'}

emotions = ['joy', 'sadness', 'anger', 'fear', 'love', 'surprise']

def get_emotion(string):
    response = requests.post('https://EmotionAPI.matthewzhang8.repl.co/predict', json =[string])
    emotion = response.json()
    return(emotion['prediction'][0])