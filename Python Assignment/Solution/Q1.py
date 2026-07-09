def asterisks(): # Top and bottom border
    return ("*" * 50)

def wrap_with_border(text):
    line = "*{:^46}*".format(text)
    return line


def generate_invites(guest_list, event_details):
    all_invites ={}
    for guest in guest_list:
        #Checking length of Name with Dear and affiliation and turncating accordingly
        name = "Dear {}".format(guest['Name'])
        if len(name) > 46:
            name = name[:43] + "..."
        affiliation = guest['Affiliation']
        if len(affiliation) > 46:
            affiliation = affiliation[:43] + "..."

        card = asterisks() + "\n"
        card += wrap_with_border("Saraswati Puja Invitation") + "\n"
        card += wrap_with_border("Utkal Parishad, IIT Kanpur") + "\n"
        card += wrap_with_border("") + "\n"
        card += wrap_with_border(name) + "\n"
        card += wrap_with_border(affiliation)+ "\n"
        card += wrap_with_border("") + "\n"
        card += wrap_with_border("Date: {}".format(event_details['Date'])) + "\n"
        card += wrap_with_border("Venue: {}".format(event_details['Venue'])) + "\n"
        card += wrap_with_border("Schedule: {}".format(event_details['Schedule']))+ "\n"
        card += asterisks()
        email_key = guest['Email']
        all_invites[email_key] = card
    return all_invites


#TO SEE OUTPUT
#if __name__ == "__main__":
#    guests = [
#        {'Name': 'Aman', 'Affiliation': 'CSE Dept', 'Email': 'aman@iitk.ac.in'},
#        {'Name': 'Dr. Very Long Name That Definitely Exceeds The Character Limit',
#        'Affiliation': 'Physics Department With Long Name',
#         'Email': 'dr.long@iitk.ac.in'}
#    ]
#
#    details = {
#        'Date': 'Feb 14, 2026',
#        'Venue': 'Community Hall',
#        'Schedule': '10:00 AM'
#    }
#
#    invites = generate_invites(guests, details)
#
#    for email, card in invites.items():
#       print(f"\n--- Invite for {email} ---\n")
#       print(card)