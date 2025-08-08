user = "root"
password = "123456"
host = "localhost"
port = "3306"
database_name = "MVC"

tables_constrains = {
    'Location': {
        'locationID': ('KEY', None),
        'type': ('VARCHAR', ['Head', 'Branch']),
        'name': ('VARCHAR', 'Required'),
        'address': ('VARCHAR', None),
        'city': ('VARCHAR', None),
        'province': ('VARCHAR', None),
        'postalCode': ('VARCHAR', None),
        'phoneNumber': ('VARCHAR', None),
        'webAddress': ('VARCHAR', None),
        'maxCapacity': ('INT', None),
    },
    'FamilyMember': {
        'familyMemberID': ('KEY', None),
        'firstName': ('VARCHAR', 'Required'),
        'lastName': ('VARCHAR', 'Required'),
        'DOB': ('DATE', 'Required'),
        'SSN': ('VARCHAR', 'Required'),
        'medicareNumber': ('VARCHAR', None),
        'phoneNumber': ('VARCHAR', None),
        'address': ('VARCHAR', None),
        'city': ('VARCHAR', None),
        'province': ('VARCHAR', None),
        'postalCode': ('VARCHAR', None),
        'email': ('VARCHAR', None),
    },
    'ClubMember': {
        'memberID': ('KEY', None),
        'firstName': ('VARCHAR', 'Required'),
        'lastName': ('VARCHAR', 'Required'),
        'DOB': ('DATE', 'Required'),
        'height': ('DECIMAL', None),
        'weight': ('DECIMAL', None),
        'SSN': ('VARCHAR', 'Required'),
        'medicareNumber': ('VARCHAR', None),
        'phoneNumber': ('VARCHAR', None),
        'address': ('VARCHAR', None),
        'city': ('VARCHAR', None),
        'province': ('VARCHAR', None),
        'postalCode': ('VARCHAR', None),
        'memberStatus': ('VARCHAR', ['Minor', 'Major']),
        'email': ('VARCHAR', None),
    },
    'Personnel': {
        'personnelID': ('KEY', None),
        'SSN': ('VARCHAR', "Required"),
        'firstName': ('VARCHAR', None),
        'lastName': ('VARCHAR', None),
        'DOB': ('DATE', None),
        'medicareNumber': ('VARCHAR', None),
        'phoneNumber': ('VARCHAR', None),
        'address': ('VARCHAR', None),
        'city': ('VARCHAR', None),
        'province': ('VARCHAR', None),
        'postalCode': ('VARCHAR', None),
        'email': ('VARCHAR', None),
        'role': (
            'VARCHAR',
            ['Administrator', 'Captain', 'Coach', 'Assistant Coach', 'Other'],
        ),
        'mandate': ('VARCHAR', ['Volunteer', 'Salaried']),
    },
    'Hobbies': {
        'hobbyName': ('KEY', None),
    },
    'TeamFormation': {
        'sessionID': ('KEY', None),
        'sessionType': ('VARCHAR', ['Game', 'Training']),
        'dateTime': ('DATETIME', None),
        'address': ('VARCHAR', None),
    },
    'Payment': {
        'paymentID': ('INT', None),
        'paymentDate': ('DATE', None),
        'amount': ('DECIMAL', None),
        'paymentMethod': ('VARCHAR', ['Cash', 'Debit', 'Credit Card']),
        'membershipYear': ('INT', None),
    },
    'Team': {
        'sessionID': ('KEY', None),
        'teamNumber': ('KEY', None),
        'teamName': ('VARCHAR', 'Required'),
        'score': ('INT', None),
        'gender': ('VARCHAR', ['Male', 'Female']),
    },
    'WorksAt': {
        'personnelID': ('KEY', None),
        'locationID': ('KEY', None),
        'startDate': ('KEY', None),
        'endDate': ('DATE', None),
    },
    'AssociatedWith': {
        'familyMemberID': ('KEY', None),
        'locationID': ('KEY', None),
        'startDate': ('KEY', None),
        'endDate': ('DATE', None),
    },
    'Registers': {
        'memberID': ('KEY', None),
        'familyMemberID': ('KEY', None),
        'startDate': ('KEY', None),
        'endDate': ('DATE', None),
        'relationshipType': (
            'VARCHAR',
            [
                'Father', 'Mother', 'Grandfather', 'Grandmother', 'Tutor',
                'Partner', 'Friend', 'Other'
            ],
        ),
    },
    'HasHobby': {
        'memberID': ('KEY', None),
        'hobbyName': ('KEY', None),
    },
    'BelongTo': {
        'memberID': ('KEY', None),
        'locationID': ('KEY', None),
        'startDate': ('KEY', None),
        'endDate': ('DATE', None),
    },
    'PlaysIn': {
        'memberID': ('INT', None),
        'sessionID': ('INT', None),
        'teamNumber': ('INT', None),
        'playerRole': ('VARCHAR', None),
    },
    'BasedAt': {
        'sessionID': ('KEY', None),
        'teamNumber': ('KEY', None),
        'locationID': ('KEY', None),
    },
    'MakePayment': {
        'paymentID': ('INT', None),
        'memberID': ('INT', 'Required'),
        'installmentNumber': ('INT', [1, 2, 3, 4]),
    },
    'SecondaryFM': {
        'familyMemberID': ('KEY', None),
        'firstName': ('VARCHAR', None),
        'lastName': ('VARCHAR', None),
        'phoneNumber': ('VARCHAR', None),
    },
    'EmergencyContactFor': {
        'familyMemberID': ('KEY', None),
        'memberID': ('KEY', None),
        'relationshipType': (
            'VARCHAR',
            [
                'Father', 'Mother', 'Grandfather', 'Grandmother', 'Tutor',
                'Partner', 'Friend', 'Other'
            ],
        ),
    },
    'CoachedBy': {
        'personnelID': ('KEY', None),
        'sessionID': ('KEY', None),
        'teamNumber': ('KEY', None),
    },
    'Log': {
        'logID': ('INT', None),
        'emailDate': ('DATETIME', None),
        'senderEmail': ('VARCHAR', None),
        'receiverEmail': ('VARCHAR', None),
        'subject': ('VARCHAR', None),
        'bodySnippet': ('VARCHAR', None),
    },
}
