DECISION_TREE = [
    {
        'sleep': 'medium', 'fatigue': 'high',
        'pain': 'high', 'distress': 'high',
        'intervention':
        [
        ['zucker', 'Dr. David Zucker specializes in helping cancer patients with symptoms. Let\'s give a listen.'],
        ['soothing_music', 'Soothing music is a great way to leave the world behind for awhile. Would you like to try some?'],
        ['soothing_music', 'They say music soothes the soul. How about we try some soothing music and see if you like it.']
        ]
    }

    # the rest dictionaries in the DECISION_TREE are deleted to protect Intellectual Property 
]




MEDIA_TYPE = {
    'soothing_music': 'audio',
    'exercise': 'video'
    # the rest dictionaries in the DECISION_TREE are deleted to protect Intellectual Property 
}





#the sequence of urls in each intervention's list matters!!!
MEDIA_FILE = {
    'soothing_music': 
        [
            'https://XYZ.s3.us-east-2.amazonaws.com/ABC/DEF.mp3'

        ]
    # the rest dictionaries in the DECISION_TREE are deleted to protect Intellectual Property 
}


