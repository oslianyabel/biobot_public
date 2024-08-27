from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import os, json, requests, time
from datetime import datetime
from functions import *
import mongo

WORDS_LIMIT = 1599

def date_diff(date1, date2):
    # Asegurarse de que ambas fechas sean del tipo datetime
    if isinstance(date1, str):
        date1 = datetime.fromisoformat(date1)
    if isinstance(date2, str):
        date2 = datetime.fromisoformat(date2)
    
    # Calcular la diferencia en años
    diff = abs((date2 - date1).days)
    
    return diff

def send_twilio_message(body, from_, to):
    if len(body) > WORDS_LIMIT:
        print("Mensaje acortado por exceso de caracteres.")
        body = body[:WORDS_LIMIT]
        
    twilio_client = Client(os.getenv('ACCOUNT_SID'), os.getenv('AUTH_TOKEN'))
    twilio_client.messages.create(
        body=body,
        from_=from_,
        to=to
    )
    print("Mensaje Enviado!")
    print(f"-Assistant: {body}")
    
def send_twilio_message2(body, from_, to):
    if len(body) > WORDS_LIMIT:
        print("Mensaje acortado por exceso de caracteres.")
        body = body[:WORDS_LIMIT]
    
    retries = 3
    delay = 0.5  # 500ms delay
    twilio_client = Client(os.getenv('ACCOUNT_SID'), os.getenv('AUTH_TOKEN'))

    for attempt in range(1, retries + 1):
        try:
            twilio_client.messages.create(
                body=body,
                from_=from_,
                to=to
            )
            print("Mensaje Enviado!")
            print(f"-Assistant: {body}")
            return True
        except Exception as error:
            print(f"Attempt {attempt} failed:", error)
            if attempt < retries:
                print(f"Retrying in {delay * 1000}ms...")
                time.sleep(delay)  # Wait before retrying
            else:
                print("All attempts to send the message failed.")
                return False
    
def clear_history(user_number):
    mongo.conversations.delete_one({"number": user_number})
    print("Historial eliminado")
    send_twilio_message(
        body = "Historial eliminado.",
        from_=f'whatsapp:+{mongo.get_bot_number()}',
        to='whatsapp:+{}'.format(user_number)
    )

def generate_response(openai_client, conversation, tools):
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",#gpt-3.5-turbo-0125 alternativo
        messages=conversation,
        tools=tools,
        tool_choice="auto",
    )
    return response
        
def tools_call(response, conversation, available_functions, user_number):
    tool_calls = response.choices[0].message.tool_calls
    conversation_copy = conversation.copy()
    conversation_copy.append(response.choices[0].message)
    
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        print(function_name)
        
        slow_functions = ["top_customer", "sales_report", "customer_with_pending_orders_to_pay", "pending_invoices_to_pay"]
        
        if function_name in slow_functions:
            send_twilio_message(
                body="Estoy procesando su solicitud, por favor espere...",
                from_=f"whatsapp:+{mongo.get_bot_number()}",
                to="whatsapp:+{}".format(user_number)
            )
        
        if function_name == 'clear_chat':
            clear_history(user_number)
            return None
        
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)
        print(function_args)
        function_response = function_to_call(**function_args)
        conversation_copy.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            }
        )
        
    return conversation_copy

        
def reply_text(ans, conversation, user_number):
    conversation.append({"role": "assistant", "content": ans, "date": datetime.now().strftime('%Y-%m-%d')})
    mongo.update_conversation(user_number, conversation)

    send_twilio_message2(
        body=str(ans),
        from_=f'whatsapp:+{mongo.get_bot_number()}',
        to='whatsapp:+{}'.format(user_number)
    )
    
    return str(MessagingResponse())

def media_handler(request):
    media_url = request.values.get("MediaUrl0")
    media_content_type = request.values.get("MediaContentType0")
    sender = request.values.get("From")
    message_sid = request.values.get("MessageSid")
    
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    # Descargar y guardar el archivo
    response = requests.get(media_url)
    file_type = media_content_type.split('/')[0]
    file_extension = media_content_type.split('/')[1]
    file_name = f"{message_sid}.{file_extension}"
    file_path = os.path.join("downloads", file_name)

    with open(file_path, 'wb') as file:
        file.write(response.content)

    print(f"Received media from {sender}")
    print(f"Media Content Type: {media_content_type}")
    print(f"File saved to: {file_path}")

    if file_type == "application":
        file_type = "documento"
    
    return file_type