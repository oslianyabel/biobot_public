from flask import Flask, request
from openai import OpenAI
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from datetime import datetime
from waitress import serve
import mongo, tools, utils, system, os, re

load_dotenv()

def crear_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

    @app.route('/whatsapp', methods=['POST'])
    def whatsapp_reply():
        incoming_msg = request.form['Body'].strip()
        user_number = re.sub(r'^whatsapp:\+', '', request.values.get('From', ''))
        admin_users = mongo.get_admin_users()
        conversation = mongo.get_conversation(user_number)
        num_media = int(request.values.get("NumMedia", 0))

        if not incoming_msg and not num_media:
            print("Mensaje no recibido.")
            ans = MessagingResponse()
            ans.message("Mensaje no recibido.")
            return str(ans)
        
        if not conversation:
            sys_msg = system.system_admin if user_number in admin_users else system.system
            if user_number in admin_users:
                user_name = mongo.get_user_name(user_number)
                sys_msg += f"El usuario se llama {user_name}. Refiérete siempre al él por su nombre.\n"
            conversation = [
                {"role": "system", "content": sys_msg, "date": datetime.now().strftime('%Y-%m-%d')},
            ]
            print("Inicio de Conversación.")
        
        if num_media:
            file_type = utils.media_handler(request)
            conversation.append({
                "role": "user", 
                "content": incoming_msg + "(Fecha: {})({} enviado)".format(datetime.now().strftime('%Y-%m-%d'), file_type), 
                "date": datetime.now().strftime('%Y-%m-%d')
            })
            mongo.update_conversation(user_number, conversation)
        else:
            conversation.append({
                "role": "user", 
                "content": incoming_msg + "(Fecha: {})".format(datetime.now().strftime('%Y-%m-%d')), 
                "date": datetime.now().strftime('%Y-%m-%d')
            })
            mongo.update_conversation(user_number, conversation)

        print("Mensaje Recibido!")
        print(f"-User: {incoming_msg}")
        
        available_tools = tools.admin_tools if user_number in admin_users else tools.user_tools
        available_functions = tools.admin_available_functions if user_number in admin_users else tools.user_available_functions
        if user_number in admin_users:
            print("Permisos de Administrador")
        else:
            print("Permisos de Usuario")
            
        response = utils.generate_response(openai_client, conversation, available_tools)
        tool_calls = response.choices[0].message.tool_calls
        if tool_calls:
            print("Tool calls")
            conversation_ext = utils.tools_call(response, conversation, available_functions, user_number)
            if not conversation_ext:#clear_chat
                return str(MessagingResponse())
            
            response = utils.generate_response(openai_client, conversation_ext, available_tools)
            ans = response.choices[0].message.content
            conversation.append({"role": "assistant", "content": ans, "date": datetime.now().strftime('%Y-%m-%d')})
            mongo.update_conversation(user_number, conversation)
            
            utils.send_twilio_message2(
                body=str(ans),
                from_=f'whatsapp:+{mongo.get_bot_number()}',
                to='whatsapp:+{}'.format(user_number)
            )
            
            return str(MessagingResponse())
        else:
            ans = response.choices[0].message.content
            return utils.reply_text(ans, conversation, user_number)
            
    return app

if __name__ == '__main__':
    app = crear_app()
    #app.run(debug=True, host='0.0.0.0', port=3024)
    serve(app, host='0.0.0.0', port=3024)