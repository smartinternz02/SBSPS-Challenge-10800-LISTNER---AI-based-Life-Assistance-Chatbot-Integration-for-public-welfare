from flask import Flask, request, jsonify
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

app = Flask(_name_)

# IBM Watson Assistant credentials
api_key = "NSIS3RtrGx4I2lmPN-kibu6MH8F15_5iBQvALpBLr3Oa"
assistant_url = "https://api.au-syd.assistant.watson.cloud.ibm.com/instances/9b915b88-3c81-4e42-a63b-1462b40fd383"
assistant_id = "AC14f92a06db220777028233f216a5649f"

# Create an IAM Authenticator
authenticator = IAMAuthenticator(api_key)

# Create an Assistant instance
assistant = AssistantV2(
    version='2021-06-14',  # Adjust the version as needed
    authenticator=authenticator
)

# Set the service URL
assistant.set_service_url(assistant_url)

@app.route('/chat', methods=['POST'])
def chat_with_assistant():
    try:
        user_input = request.json['message']
        # Create a session
        response = assistant.create_session(
            assistant_id=assistant_id
        ).get_result()

        session_id = response['session_id']

        # Send a message to the assistant
        response = assistant.message(
            assistant_id=assistant_id,
            session_id=session_id,
            input={
                'message_type': 'text',
                'text': user_input
            }
        ).get_result()

        # Extract and return the assistant's response
        assistant_response = response['output']['generic'][0]['text']

        # Close the session
        assistant.delete_session(
            assistant_id=assistant_id,
            session_id=session_id
        )

        return jsonify({"response": assistant_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if _name_ == '_main_':
    app.run(debug=True)