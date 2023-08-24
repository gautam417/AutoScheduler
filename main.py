from flask import Flask, request
from twilio.twiml.voice_response import Gather, VoiceResponse
import openai

app = Flask(__name__)
openai.api_key = os.environ.get('OPENAI_SECRET_KEY')


def generate_question(prompt):
    openai_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    return openai_response.choices[0].text

@app.route('/call', methods=['POST'])
def handle_call():
    response = VoiceResponse()
    gather = Gather(numDigits=1, action='/menu_options')
    gather.say("Welcome to your AutoScheduler Medical AI Assistant. Press 1 to start scheduling an appointment, or press 2 to hear this message again.")
    response.append(gather)
    return str(response)

@app.route('/menu_options', methods=['POST'])
def menu_options():
    selected_option = request.values.get('Digits', '')
    next_question = "Please provide your full name, date of birth, and address." if selected_option == '1' else "Press 1 to start scheduling an appointment, or press 2 to hear this message again."
    response = VoiceResponse()
    action_url = '/collect_personal_info' if selected_option == '1' else '/call'
    gather = Gather(input='speech', action=action_url)
    gather.say(next_question)
    response.append(gather)
    return str(response)

@app.route('/collect_personal_info', methods=['POST'])
def collect_personal_info():
    response = VoiceResponse()
    gather = Gather(input='speech', action='/collect_insurance')
    gather.say("Please tell me your insurance provider and ID number.")
    response.append(gather)
    return str(response)

@app.route('/collect_insurance', methods=['POST'])
def collect_insurance():
    response = VoiceResponse()
    gather = Gather(input='speech', action='/collect_referral')
    gather.say("Do you have a referral from another doctor? If so, please provide the details.")
    response.append(gather)
    return str(response)

@app.route('/collect_referral', methods=['POST'])
def collect_referral():
    response = VoiceResponse()
    gather = Gather(input='speech', action='/collect_complaint')
    gather.say("What is the chief medical complaint or reason for the visit?")
    response.append(gather)
    return str(response)

@app.route('/collect_complaint', methods=['POST'])
def collect_complaint():
    response = VoiceResponse()
    gather = Gather(input='speech', action='/collect_contact_info')
    gather.say("Please provide your contact information such as phone number and email address.")
    response.append(gather)
    return str(response)

@app.route('/collect_contact_info', methods=['POST'])
def collect_contact_info():
    response = VoiceResponse()
    gather = Gather(input='speech', action='/final_schedule')
    gather.say("Please select one of our top medical providers in your area. Provider A at 10 AM, Provider B at 2 PM, or Provider C at 4 PM.")
    response.append(gather)
    return str(response)

@app.route('/final_schedule', methods=['POST'])
def final_schedule():
    response_text = request.values.get('SpeechResult')
    response = VoiceResponse()
    response.say(f"You've successfully scheduled an appointment with {response_text}. Thank you for using our service!")
    return str(response)

if __name__ == '__main__':
    app.run(debug=True)
