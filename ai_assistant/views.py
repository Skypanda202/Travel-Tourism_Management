from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def ai_chat(request):

    message = request.data.get("message")

    # Dummy AI Logic
    if "goa" in message.lower():

        reply = (
            "You can visit Baga Beach, "
            "Calangute Beach, and "
            "Anjuna Beach."
        )

    elif "hill" in message.lower():

        reply = (
            "You should visit Manali, "
            "Darjeeling, or Ooty."
        )

    else:

        reply = (
            "Please tell me your "
            "travel interests."
        )

    return Response({
        "reply": reply
    })