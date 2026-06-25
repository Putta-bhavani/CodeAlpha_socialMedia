from django.shortcuts import render

def chatbot(request):

    reply = ""

    if request.method == "POST":

        message = request.POST.get("message")

        if message.lower() == "hi":
            reply = "Hello 👋 How can I help you?"

        elif message.lower() == "hello":
            reply = "Hi 😊 Nice to meet you."

        elif message.lower() == "what is ai":
            reply = "AI stands for Artificial Intelligence."
        elif message.lower() == "what is like ":
            reply = "It is the impression of people."

        elif message.lower() == "bye":
            reply = "Goodbye 👋"

        else:
            reply = "Sorry, I don't understand."

    return render(request, "chatbot.html", {
        "reply": reply
    })