from flask import Flask, request
from twilio.twiml.voice_response import Gather, VoiceResponse

app = Flask(__name__)

@app.route('/call', methods=['POST'])
def handle_call():
    response = VoiceResponse()
    gather = Gather(numDigits=1, action='/menu_options')
    gather.say('Welcome to the Auto Scheduler Medical AI Assistant. Press 1 to schedule an appointment or 2 to repeat this intro message.')
    response.append(gather)
    return str(response)

@app.route('/menu_options', methods=['POST'])
def menu_options():
    selected_option = request.values.get('Digits', '')
    response = VoiceResponse()

    if selected_option == '1':
        gather = Gather(input='speech', action='/collect_personal_info')
        gather.say('Please provide your name, date of birth, and place of residence.')
        response.append(gather)
    else:
        response.redirect('/call')

    return str(response)

@app.route('/collect_personal_info', methods=['POST'])
def collect_personal_info():
    # Process personal information
    response = VoiceResponse()
    gather = Gather(input='speech', action='/collect_insurance')
    gather.say('Please provide your insurance payer name and ID.')
    response.append(gather)
    return str(response)

@app.route('/collect_insurance', methods=['POST'])
def collect_insurance():
    # Process insurance information
    response = VoiceResponse()
    gather = Gather(input='speech', action='/collect_referral')
    gather.say('Do you have a referral? If yes, please provide the referral details.')
    response.append(gather)
    return str(response)

@app.route('/collect_referral', methods=['POST'])
def collect_referral():
    # Process referral information
    response = VoiceResponse()
    gather = Gather(input='speech', action='/collect_complaint')
    gather.say('Please provide the chief medical complaint or reason for your visit.')
    response.append(gather)
    return str(response)

@app.route('/collect_complaint', methods=['POST'])
def collect_complaint():
    # Process complaint information
    response = VoiceResponse()
    gather = Gather(input='speech', action='/collect_contact_info')
    gather.say('Please provide your contact information.')
    response.append(gather)
    return str(response)

@app.route('/collect_contact_info', methods=['POST'])
def collect_contact_info():
    # Process contact information
    response = VoiceResponse()
    gather = Gather(input='speech', action='/final_schedule')
    gather.say('Dr. Smith is available at 10 AM on Monday, and Dr. Johnson at 2 PM on Tuesday. Press 1 for Dr. Smith or 2 for Dr. Johnson.')
    response.append(gather)
    return str(response)

@app.route('/final_schedule', methods=['POST'])
def final_schedule():
    selected_option = request.values.get('Digits', '')
    response = VoiceResponse()

    if selected_option == '1':
        response.say('Your appointment with Dr. Smith has been scheduled for 10 AM on Monday. Thank you!')
    else:
        response.say('Your appointment with Dr. Johnson has been scheduled for 2 PM on Tuesday. Thank you!')

    return str(response)

if __name__ == '__main__':
    app.run(debug=True)
