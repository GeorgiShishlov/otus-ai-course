from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import SurveyAnswer

QUESTIONS = [
    {'id': 1, 'text': 'Что такое замыкание (closure) в JavaScript?'},
    {'id': 2, 'text': 'Объясните разницу между var, let и const.'},
    {'id': 3, 'text': 'Что такое Promise и для чего он используется?'},
    {'id': 4, 'text': 'Чем отличается == от === в JavaScript?'},
    {'id': 5, 'text': 'Что такое REST API и какие у него основные принципы?'},
]


@api_view(['GET'])
def questions(request):
    return Response(QUESTIONS)


@api_view(['GET', 'POST'])
def answers(request):
    if request.method == 'GET':
        data = list(SurveyAnswer.objects.values('id', 'answers', 'created_at'))
        return Response(data)

    payload = request.data
    if not isinstance(payload, list):
        return Response({'error': 'Expected a list of answers'}, status=status.HTTP_400_BAD_REQUEST)
    SurveyAnswer.objects.create(answers=payload)
    return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
