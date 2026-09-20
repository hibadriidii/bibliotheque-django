from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .services import get_chatbot_response


def chatbot_view(request):
    suggestions = [
        "Est-ce que le livre avec l'ID 1 existe ?",
        "Quels livres de Victor Hugo sont disponibles ?",
        "Je veux un roman romantique facile à lire.",
        "Combien de livres sont disponibles en ce moment ?",
        "Recommande-moi un livre d'informatique.",
        "Quels livres sont actuellement empruntés ?",
    ]
    return render(request, 'chatbot/chatbot.html', {'suggestions': suggestions})


@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()
            if not message:
                return JsonResponse({'error': 'Message vide'}, status=400)

            response = get_chatbot_response(message)
            return JsonResponse({'response': response})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON invalide'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
