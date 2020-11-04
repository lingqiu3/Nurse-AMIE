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
    },
    {
        'sleep': 'medium', 'fatigue': 'medium',
        'pain': 'high', 'distress': 'high',
        'intervention':
        [
        ['soothing_music', 'Let\'s try and leave the real world behind for a little bit. I have some nice music that will take you to a wonderful place.'],
        ['soothing_music', 'They say music soothes the soul. How about we try some soothing music and see if you like it.'],
        ['guided_relaxation', 'Today we are going to recharge the mind and soul. Come with me and learn some new relaxation skills.']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'low',
        'pain': 'high', 'distress': 'high',
        'intervention':
        [
        ['hayes', 'Dr. Michael Hayes is a clinical psychologist at Penn State Cancer Institute. He has a way with words. We think he can help.'],
        ['soothing_music', 'Music can distract, delight, and shift your focus.  Let\'s take a listen.'],
        ['guided_relaxation', 'I know this really great teacher. I am going to share with you their method of relaxation.']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'high',
        'pain': 'medium', 'distress': 'high',
        'intervention':
        [
        ['soothing_music', 'Let\'s try and leave the real world behind for a little bit. I have some nice music that will take you to a wonderful place.'],
        ['zucker', 'Dr. David Zucker helps those living with cancer see their journey in a new light.  Listen.'],
        ['zucker', 'Sometimes it\'s helpful to hear an expert talk about the cancer experience with new words. let\'s listen.']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'medium',
        'pain': 'medium', 'distress': 'high',
        'intervention':
        [
        ['connect', 'Sometimes it is helpful to talk with others who can truly understand you. Would you like to connect with other women with metastatic disease?'],
        ['strengthening', 'Let\'s get that body moving. Are you ready?'],
        ['hayes', 'Based on what you\'ve told me, I think that a session with Dr. Michael Hayes, psychologist, might be just the ticket.  Let\'s try.']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'low',
        'pain': 'medium', 'distress': 'high',
        'intervention':
        [
        ['soothing_music', 'I have just the right selection to take you to another place. I hope it makes you feel better.'],
        ['hayes', 'Based on what you\'ve told me, I think that a session with Dr. Michael Hayes, psychologist, might be just the ticket.  Let\'s try.'],
        ['soothing_music', 'I have just the right selection to take you to another place. I hope it makes you feel better.']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'high',
        'pain': 'low', 'distress': 'high',
        'intervention':
        [
        ['walking', 'Did you know that getting moving is the number one recommendation for addressing fatigue?  Let\'s try it!'],
        ['strengthening', 'Getting the blood pumping makes us feel better. Are you ready to try some movement today?'],
        ['zucker', 'Well, let\'s see. Hm. we could. hm. yes, yes, I know:  some words of wisdom from Dr David Zucker.  Listen up!']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'medium',
        'pain': 'low', 'distress': 'high',
        'intervention':
        [
        ['hayes', 'Today Dr. Michael Hayes will provide some guidance that we hope will help in coping with symptoms.'],
        ['hayes', 'Today Dr. Michael Hayes will provide some guidance that we hope will help in coping with symptoms.'],
        ['guided_relaxation', 'Today we are going to recharge the mind and soul. Come with me and learn some new relaxation skills.']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'low',
        'pain': 'low', 'distress': 'high',
        'intervention':
        [
        ['hayes', 'Dr. Michael Hayes might have some pearls of wisdom that would help you today.  Let\'s listen.'],
        ['balance', 'They say moving does a body good. Let\'s test that theory out. Today I\'m asking you to reach your step counts and complete this movement session.'],
        ['strengthening', 'They say moving does a body good. Let\'s test that theory out. Today I\'m asking you to reach your step counts and complete this movement session.'],
        ['soothing_music', 'They say music soothes the soul. How about we try some soothing music and see if you like it.']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'high',
        'pain': 'high', 'distress': 'medium',
        'intervention':
        [
        ['balance', 'Sweatin to the oldies is the theme of the day. Let\'s get moving. Reach your step counts, and try this movement session.'],
        ['stretching', 'They say moving does a body good. Let\'s test that theory out. Today I\'m asking you to reach your step counts and complete this movement session.'],
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'medium',
        'pain': 'high', 'distress': 'medium',
        'intervention':
        [
        ['guided_relaxation', 'Today we are going to recharge the mind and soul. Come with me and learn some new relaxation skills.'],
        ['strengthening', 'Getting the blood pumping makes us feel better. Are you ready to get down and get funky?  Awesome!  Walk more to reach your step counts, and complete this movement session.'],
        ['balance', 'Getting the blood pumping makes us feel better. Are you ready to get down and get funky?  Awesome!  Walk more to reach your step counts, and complete this movement session.']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'low',
        'pain': 'high', 'distress': 'medium',
        'intervention':
        [
        ['guided_relaxation', 'Well, I\'m no expert, but I know someone who is.  How about we let the experts teach you some relaxation techniques.'],
        ['walking', 'Let\'s get that body moving. Are you ready?'],
        ['soothing_music', 'I have a few new selections for you to listen to. Are you ready?']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'high',
        'pain': 'medium', 'distress': 'medium',
        'intervention':
        [
        ['balance', 'Getting the blood pumping makes us feel better. Are you ready to get down and get funky?  Awesome!  Walk more to reach your step counts, and complete this movement session.'],
        ['strengthening', 'They say moving does a body good. Let\'s test that theory out. Today I\'m asking you to reach your step counts and complete this movement session.'],
        ['zucker', 'Well, let\'s see. Hm. we could. hm. yes, yes, I know:  some words of wisdom from Dr David Zucker.  Listen up!']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'medium',
        'pain': 'medium', 'distress': 'medium',
        'intervention':
        [
        ['balance', 'Hey, for today, let\'s try increasing your steps and completing a movement session designed with you in mind.  Let us know how all these sessions are working for you!'],
        ['strengthening', 'Hey, for today, let\'s try increasing your steps and completing a movement session designed with you in mind.  Let us know how all these sessions are working for you!'],
        ['guided_relaxation', 'Today we are going to walk through one method of relaxation. Are you ready to learn?'], 
        ['zucker', 'Dr David Zucker has some tips that might help you manage the symptoms you are feeling. Would you like to have a look?']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'low',
        'pain': 'medium', 'distress': 'medium',
        'intervention':
        [
        ['strengthening', 'Step 1.  Step more.  Step 2.  Try this movement session, designed with you in mind.  Step 3.  Pat yourself on the back.'], 
        ['balance', 'They say moving does a body good. Let\'s test that theory out. Today I\'m asking you to reach your step counts and complete this movement session.'], 
        ['guided_relaxation', 'Today we are going to walk through one method of relaxation. Are you ready to learn?']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'high',
        'pain': 'low', 'distress': 'medium',
        'intervention':
        [
        ['zucker', 'Dr. David Zucker once told me that every cancer patient has WAY more healthy cells than cancer cells. pretty amazing idea, right?  Lets see what else he has to say...'],
        ['balance', 'Scientists say that movement will make you sleep better, and help with symptoms.  Let\'s test out that theory by increasing your steps and this movement session!'],
        ['strengthening', 'The theme of the day is MOVEMENT. Let\'s get moving. ']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'medium',
        'pain': 'low', 'distress': 'medium',
        'intervention':
        [
        ['walking', 'Scientists say that movement will make you sleep better, and help with symptoms.  Let\'s test out that theory!'], 
        ['soothing_music', 'I have a few new selections for you to listen to. Are you ready?'], 
        ['walking', 'The theme of the day is MOVEMENT. Let\'s get moving. ']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'low',
        'pain': 'low', 'distress': 'medium',
        'intervention':
        [
        ['walking', 'Let\'s get that body moving. Are you ready?'],
        ['strengthening', 'Let\'s get that body moving. Are you ready?'], 
        ['hayes', 'If there\'s one thing that I am sure of, it\'s the expertise of our cancer institute psychologist.  Let\'s see what he might have to say to you.'], 
        ['guided_relaxation', 'Experts tell us that meditation and relaxation really changes our bodies for the better.  Let\'s give it a try!']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'high',
        'pain': 'high', 'distress': 'low',
        'intervention':
        [
        ['guided_relaxation', 'Experts tell us that meditation and relaxation really changes our bodies for the better.  Let\'s give it a try!'],
        ['balance', 'Let\'s get that body moving. Are you ready?'],
        ['stretching', 'Let\'s get that body moving. Are you ready?'],
        ['hayes', 'Never fear!  Dr. Michael Hayes is here!  He\'s the clinical psychologist at Penn State\'s Cancer institute.  I bet his sage wisdom will help...']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'medium',
        'pain': 'high', 'distress': 'low',
        'intervention':
        [
        ['hayes', 'Is there EVER a time when helpful guidance from a seasoned professional with experience in what ails you doesn\'t help?  Yeah, I thought not.  Let\'s listen.'],
        ['balance', 'Let\'s get that body moving. Are you ready?'],
        ['stretching', 'Let\'s get that body moving. Are you ready?']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'low',
        'pain': 'high', 'distress': 'low',
        'intervention':
        [
        ['hayes', 'Seems you are dealing with some symptoms.  Hm... how about some guidance from psychologist Dr. Michael Hayes on how to cope?  Let\'s listen.'],
        ['balance', 'Let\'s get that body moving. Are you ready?'],
        ['stretching', 'Let\'s get that body moving. Are you ready?'],
        ['guided_relaxation', 'How about we let the experts teach you some relaxation techniques.']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'high',
        'pain': 'medium', 'distress': 'low',
        'intervention':
        [
        ['walking', 'Scientists say that movement will make you sleep better, and help with symptoms.  Let\'s test out that theory!'],
        ['balance', 'Maybe getting your blood pumping a little might make you feel better. Can we try a movement routine designed just for you?'],
        ['strengthening', 'Getting you off the couch is the theme of the day. Let\'s get moving. ']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'medium',
        'pain': 'medium', 'distress': 'low',
        'intervention':
        [
        ['strengthening', 'Scientists say that movement will make you sleep better, and help with symptoms.  Let\'s test out that theory!'],
        ['walking', 'Scientists say that movement will make you sleep better, and help with symptoms.  Let\'s test out that theory!'], 
        ['strengthening', 'Getting the blood pumping makes us feel better. Are you ready to get moving today?']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'low',
        'pain': 'medium', 'distress': 'low',
        'intervention':
        [
        ['balance', 'Let\'s get that body moving. Are you ready?'],
        ['strengthening', 'Scientists say that movement will make you sleep better, and help with symptoms.  Let\'s test out that theory!'], 
        ['hayes', 'Is there EVER a time when helpful guidance from a seasoned professional with experience in what ails you doesn\'t help?  Yeah, I thought not.  Let\'s listen.']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'high',
        'pain': 'low', 'distress': 'low',
        'intervention':
        [
        ['walking', 'So... yes.  It\'s true.  I do have a magic 8 ball that I use to guide you.... Just kidding.  Today let\'s get moving...'],
        ['strengthening', 'What was that?  You\'d like some guidance on getting your body moving?  Well, AWESOME, \'cause I\'ve got just the thing!  Here we go!']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'medium',
        'pain': 'low', 'distress': 'low',
        'intervention':
        [
        ['walking', 'Walking is the number 1 recommendation for combatting the symptoms you are experiencing. Please look at your step goal and work toward meeting or exceeding it. '],
        ['balance', 'This might be a great day to do some movement.  Let\'s treat your trillions of healthy cells to a treat with a movement session.  Okay?'],
        ['strengthening', 'This might be a great day to do some movement.  Let\'s treat your trillions of healthy cells to a treat with a movement session.  Okay?']
        ]
    },
    {
        'sleep': 'medium', 'fatigue': 'low',
        'pain': 'low', 'distress': 'low',
        'intervention':
        [
        ['hayes', ''],
        ['balance', 'Hey, things seem to be going okay, right?  How about some movement?'],
        ['strengthening', 'Did you know that moving more can help you sleep better?  Let\'s try a movement session.']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'high',
        'pain': 'high', 'distress': 'high',
        'intervention':
        [
        ['guided_relaxation', 'Today we are going to try some guided relaxation.'],
        ['guided_relaxation', 'Today we are going to walk through one method of relaxation. Are you ready to learn?'],
        ['guided_relaxation', 'Today I would like to walk you through some relaxation techniques. How does that sound?']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'medium',
        'pain': 'high', 'distress': 'high',
        'intervention':
        [
        ['guided_relaxation', 'Today we are going to walk through one method of relaxation. Are you ready to learn?'],
        ['guided_relaxation', 'How about we let the experts teach you some relaxation techniques.'],
        ['soothing_music', 'I have a few new musical selections for you to listen to. Are you ready?']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'low',
        'pain': 'high', 'distress': 'high',
        'intervention':
        [
        ['soothing_music', 'I have a few new musical selections for you to listen to. Are you ready?'],
        ['hayes', 'Let\'s listen to clinical psychologist Michael Hayes, who has some guidance for you in dealing with the feelings that arise with symptoms.'],
        ['soothing_music', 'I have just the right selection to take you to another place. I hope it makes you feel better.']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'high',
        'pain': 'medium', 'distress': 'high',
        'intervention':
        [
        ['zucker', 'Dr. David Zucker has such a way with words. I bet he can say something to help you!'],
        ['stretching', 'Getting off the couch is the theme of the day. Let\'s get moving. '],
        ['walking', 'Getting off the couch is the theme of the day. Let\'s get moving. '],
        ['soothing_music', 'They say music soothes the soul. How about we try some soothing music and see if you like it.']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'medium',
        'pain': 'medium', 'distress': 'high',
        'intervention':
        [
        ['soothing_music', 'They say music soothes the soul. How about we try some soothing music and see if you like it.'],
        ['strengthening', 'Even if you don\'t feel like it, getting moving can really help at a time like this ... Let\'s test that theory.'],
        ['guided_relaxation', 'I have just the right selection to take you to another place. I hope it makes you feel better.']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'low',
        'pain': 'medium', 'distress': 'high',
        'intervention':
        [
        ['soothing_music', 'Music can distract, delight, and shift your focus.  Let\'s take a listen.'],
        ['walking', 'Hmm. well, let\'s see.  Even if it seems counterintuitive, I think the best thing today would be some movement.  Let\'s get off that chair!'],
        ['stretching', 'Getting off the couch is the theme of the day. Let\'s get moving. '],
        ['balance', 'Getting off the couch is the theme of the day. Let\'s get moving. ']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'high',
        'pain': 'low', 'distress': 'high',
        'intervention':
        [
        ['walking', 'Getting the blood pumping makes us feel better. Are you ready to try some movement today?'],
        ['strengthening', 'They say moving does a body good. Let\'s test that theory out. '],
        ['strengthening', 'Let\'s ease on down the road together, with a movement session.  Shall we?'],
        ['walking', 'They say moving does a body good. Let\'s test that theory out. ']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'medium',
        'pain': 'low', 'distress': 'high',
        'intervention':
        [
        ['guided_relaxation', 'Today we are going to recharge the mind and soul. Come with me and learn some new relaxation skills.'],
        ['walking', 'Getting the blood pumping makes us feel better. Are you ready to try some movement today?'],
        ['balance', 'Getting the blood pumping makes us feel better. Are you ready to try some movement today?'],
        ['soothing_music', 'I have just the right selection to take you to another place. I hope it makes you feel better.']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'low',
        'pain': 'low', 'distress': 'high',
        'intervention':
        [
        ['balance', 'Getting the blood pumping makes us feel better. Are you ready to get down and get funky?  Awesome!  Walk more to reach your step counts, and complete this movement session.'],
        ['strengthening', 'They say moving does a body good. Let\'s test that theory out. Today I\'m asking you to reach your step counts and complete this movement session.'],
        ['walking', 'Let\'s get that body moving. Are you ready?']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'high',
        'pain': 'high', 'distress': 'medium',
        'intervention':
        [
        ['soothing_music', 'I have a few new selections for you to listen to. Are you ready?'],
        ['walking', 'Let\'s get that body moving. Are you ready?'],
        ['soothing_music', 'I have a few new selections for you to listen to. Are you ready?']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'medium',
        'pain': 'high', 'distress': 'medium',
        'intervention':
        [
        ['strengthening', 'Getting the blood pumping makes us feel better. Are you ready to get down and get funky?  Awesome!  Walk more to reach your step counts, and complete this movement session.'],
        ['balance', 'Getting the blood pumping makes us feel better. Are you ready to get down and get funky?  Awesome!  Walk more to reach your step counts, and complete this movement session.'],
        ['guided_relaxation', 'Today we are going to walk through one method of relaxation. Are you ready to learn?'],
        ['soothing_music', 'I have a few new selections for you to listen to. Are you ready?']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'low',
        'pain': 'high', 'distress': 'medium',
        'intervention':
        [
        ['soothing_music', 'I have just the right selection to take you to another place. I hope it makes you feel better.'],
        ['balance', 'They say moving does a body good. Let\'s test that theory out. Today I\'m asking you to reach your step counts and complete this movement session.'],
        ['stretching', 'They say moving does a body good. Let\'s test that theory out. Today I\'m asking you to reach your step counts and complete this movement session.'],
        ['guided_relaxation', 'Well, I\'m no expert, but I know someone who is.  How about we let the experts teach you some relaxation techniques.']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'high',
        'pain': 'medium', 'distress': 'medium',
        'intervention':
        [
        ['balance', 'They say moving does a body good. Let\'s test that theory out. Today I\'m asking you to reach your step counts and complete this movement session.'],
        ['strengthening', 'They say moving does a body good. Let\'s test that theory out. Today I\'m asking you to reach your step counts and complete this movement session.'],
        ['balance', 'Getting the blood pumping makes us feel better. Are you ready to get down and get funky?  Awesome!  Walk more to reach your step counts, and complete this movement session.'],
        ['strengthening', 'Getting the blood pumping makes us feel better. Are you ready to get down and get funky?  Awesome!  Walk more to reach your step counts, and complete this movement session.']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'medium',
        'pain': 'medium', 'distress': 'medium',
        'intervention':
        [
        ['soothing_music', 'Let\'s try and leave the real world behind for a little bit. I have some nice music that will take you to a wonderful place.'],
        ['balance', 'They say moving does a body good. Let\'s test that theory out. Today, try reaching or exceeding your step goal and this movement session.'],
        ['strengthening', 'They say moving does a body good. Let\'s test that theory out. Today, try reaching or exceeding your step goal and this movement session.'],
        ['soothing_music', 'I have just the right selection to take you to another place. I hope it makes you feel better.']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'low',
        'pain': 'medium', 'distress': 'medium',
        'intervention':
        [
        ['guided_relaxation', 'Today we are going to recharge the mind and soul. Come with me and learn some new relaxation skills.'],
        ['strengthening', 'Let\'s get that body moving!  Increase your steps, and try this movement session. Are you ready?'],
        ['soothing_music', 'I have a few new selections for you to listen to. Are you ready?']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'high',
        'pain': 'low', 'distress': 'medium',
        'intervention':
        [
        ['balance', 'Maybe getting your blood pumping a little might make you feel better. Can we try increasing your steps and a movement session designed with you in mind?'],
        ['stretching', 'Maybe getting your blood pumping a little might make you feel better. Can we try increasing your steps and a movement session designed with you in mind?']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'medium',
        'pain': 'low', 'distress': 'medium',
        'intervention':
        [
        ['guided_relaxation', 'Today we are going to walk through one method of relaxation. Are you ready to learn?'],
        ['balance', 'Maybe getting your blood pumping a little might make you feel better. Can we try a movement session designed with you in mind?'],
        ['soothing_music', 'I have just the right selection to take you to another place. I hope it makes you feel better.'],
        ['strengthening', 'Maybe getting your blood pumping a little might make you feel better. Can we try a movement session designed with you in mind?']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'low',
        'pain': 'low', 'distress': 'medium',
        'intervention':
        [
        ['strengthening', 'Maybe getting your blood pumping a little might make you feel better. Can we try a movement session designed with you in mind?'],
        ['walking', 'Scientists say that movement will make you sleep better, and help with symptoms.  Let\'s test out that theory!'],
        ['strengthening', 'Scientists say that movement will make you sleep better, and help with symptoms.  Let\'s test out that theory!'],
        ['soothing_music', 'Soothing music is a great way to leave the world behind for awhile. Would you like to try some?']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'high',
        'pain': 'high', 'distress': 'low',
        'intervention':
        [
        ['balance', 'Scientists say that movement will make you sleep better, and help with symptoms.  Let\'s test out that theory!'],
        ['stretching', 'Scientists say that movement will make you sleep better, and help with symptoms.  Let\'s test out that theory!'],
        ['soothing_music', 'Soothing music is a great way to leave the world behind for awhile. Would you like to try some?'],
        ['soothing_music', 'I have a few new selections for you to listen to. Are you ready?']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'medium',
        'pain': 'high', 'distress': 'low',
        'intervention':
        [
        ['balance', 'Scientists say that movement will make you sleep better, and help with symptoms.  Let\'s test out that theory!'],
        ['stretching', 'Scientists say that movement will make you sleep better, and help with symptoms.  Let\'s test out that theory!'],
        ['soothing_music', 'Soothing music is a great way to leave the world behind for awhile. Would you like to try some?'],
        ['soothing_music', 'I have a few new selections for you to listen to. Are you ready?']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'low',
        'pain': 'high', 'distress': 'low',
        'intervention':
        [
        ['balance', 'Scientists say that movement will make you sleep better, and help with symptoms.  Let\'s test out that theory!'],
        ['stretching', 'Scientists say that movement will make you sleep better, and help with symptoms.  Let\'s test out that theory!'],
        ['soothing_music', 'Soothing music is a great way to leave the world behind for awhile. Would you like to try some?'],
        ['soothing_music', 'I have a few new selections for you to listen to. Are you ready?']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'high',
        'pain': 'medium', 'distress': 'low',
        'intervention':
        [
        ['strengthening', 'Okay.  Give me a minute.  Recent responses tell me you are fatigued AND not sleeping well.  What do do. hm. AH!  Getting your body moving will help both!  Get moving!'],
        ['balance', 'Okay.  Give me a minute.  Recent responses tell me you are fatigued AND not sleeping well.  What do do. hm. AH!  Getting your body moving will help both!  Get moving!'],
        ['strengthening', 'Maybe getting your blood pumping a little might make you feel better. Can we try a movement routine designed just for you?'],
        ['strengthening', 'Maybe getting your blood pumping a little might make you feel better. Can we try a movement routine designed just for you?'],
        ['balance', 'Maybe getting your blood pumping a little might make you feel better. Can we try a movement routine designed just for you?']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'medium',
        'pain': 'medium', 'distress': 'low',
        'intervention':
        [
        ['strengthening', 'Maybe getting your blood pumping a little might make you feel better. Can we try a movement routine designed just for you?'],
        ['soothing_music', 'I have a few new selections for you to listen to. Are you ready?'], 
        ['guided_relaxation', 'Today we are going to recharge the mind and soul. Come with me and learn some new relaxation skills.']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'low',
        'pain': 'medium', 'distress': 'low',
        'intervention':
        [
        ['soothing_music', 'I have a few new selections for you to listen to. Are you ready?'],
        ['strengthening', 'Scientists say that movement will make you sleep better, and help with symptoms.  Let\'s test out that theory!'],
        ['balance', 'Scientists say that movement will make you sleep better, and help with symptoms.  Let\'s test out that theory!'],
        ['soothing_music', 'Soothing music is a great way to leave the world behind for awhile. Would you like to try some?']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'medium',
        'pain': 'low', 'distress': 'low',
        'intervention':
        [
        ['walking', 'Let\'s get that body moving. Are you ready?'],
        ['walking', 'Walking is the number 1 recommendation for combatting the symptoms you are experiencing. Please look at your step goal and work toward meeting or exceeding it.  '],
        ['guided_relaxation', 'Today we are going to walk through one method of relaxation. Are you ready to learn?']
        ]
    },
    {
        'sleep': 'high', 'fatigue': 'low',
        'pain': 'low', 'distress': 'low',
        'intervention':
        [
        ['strengthening', 'Maybe getting your blood pumping a little might make you feel better. Can we try some movement?'],
        ['balance', 'Yep!  It\'s that time!  Here\'s some movement to try.'],
        ['guided_relaxation', 'How about, for today, we let the experts teach you some relaxation techniques?']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'high',
        'pain': 'high', 'distress': 'high',
        'intervention':
        [
        ['hayes', 'Dr. Michael Hayes is a clinical psychologist who has some tips that might help you manage the symptoms you are feeling. Would you like to have a look?'],
        ['zucker', 'Dr David Zucker has some tips that might help you manage the symptoms you are feeling. Would you like to have a look?'],
        ['hayes', 'Dr. Michael Hayes has tips that might help you manage the symptoms you are feeling. Would you like to have a look?']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'medium',
        'pain': 'high', 'distress': 'high',
        'intervention':
        [
        ['zucker', 'Dr. David Zucker is an expert in managing symptoms like the ones you are feeling. Let\'s listen.'],
        ['hayes', 'Here\'s some guidance from the clinical psychologist at Penn State\'s Cancer Institute. Are you ready?'],
        ['guided_relaxation', 'Today we are going to walk through one method of relaxation. Are you ready to learn?']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'low',
        'pain': 'high', 'distress': 'high',
        'intervention':
        [
        ['guided_relaxation', 'How about we let the experts teach you some relaxation techniques.'],
        ['soothing_music', 'They say music soothes the soul. How about we try some soothing music and see if you like it.'],
        ['guided_relaxation', 'Today we are going to walk through one method of relaxation. Are you ready to learn?']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'high',
        'pain': 'medium', 'distress': 'high',
        'intervention':
        [
        ['hayes', 'Hm.  Maybe today the right approach would be some advice from psychologist Dr. Michael Hayes.'],
        ['walking', 'I think we need to get the body moving. Want to see how this feels?'],
        ['guided_relaxation', 'Today we are going to walk through one method of relaxation. Are you ready to learn?'],
        ['stretching', 'I think we need to get the body moving. Want to see how this feels?']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'medium',
        'pain': 'medium', 'distress': 'high',
        'intervention':
        [
        ['hayes', 'Dr. Hayes is a clinical psychologist at Penn State.  I think maybe he might be able to help.'],
        ['strengthening', 'Many studies show that getting the body moving can help with mood and fatigue.  I have a program to suggest. Ready?'],
        ['hayes', 'Dr. Michael Hayes might have some pearls of wisdom that would help you today.  Let\'s listen.']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'low',
        'pain': 'medium', 'distress': 'high',
        'intervention':
        [
        ['balance', 'When things feel challenging, a sense of accomplishment can really help.  Let\'s try for some accomplishment through a movement session.'],
        ['stretching', 'When things feel challenging, a sense of accomplishment can really help.  Let\'s try for some accomplishment through a movement session.'],
        ['guided_relaxation', 'Today we are going to walk through one method of relaxation. Are you ready to learn?'],
        ['hayes', 'If there\'s one thing that I am sure of, it\'s the expertise of our cancer institute psychologist.  Let\'s see what he might have to say to you.']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'high',
        'pain': 'low', 'distress': 'high',
        'intervention':
        [
        ['walking', 'Let\'s get that body moving. Are you ready?'],
        ['strengthening', 'Let\'s get that body moving. Are you ready?'],
        ['hayes', 'Wow.  Some days are just more challenging, right?  Reviewing everything you\'ve told me, I think some pearls of wisdom from psychologist Dr. Michael Hayes could be helpful.  Let\'s try...']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'medium',
        'pain': 'low', 'distress': 'high',
        'intervention':
        [
        ['soothing_music', 'I have a few new selections for you to listen to. Are you ready?'],
        ['balance', 'They say moving does a body good. Let\'s test that theory out. Today I\'m asking you to reach your step counts and complete this movement session.'],
        ['hayes', 'If there\'s one thing that I am sure of, it\'s the expertise of our cancer institute psychologist.  Let\'s see what he might have to say to you.']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'low',
        'pain': 'low', 'distress': 'high',
        'intervention':
        [
        ['balance', 'Getting the blood pumping makes us feel better. Are you ready to get down and get funky?  Awesome!  Walk more to reach your step counts, and complete this movement session.'],
        ['strengthening', 'Getting the blood pumping makes us feel better. Are you ready to get down and get funky?  Awesome!  Walk more to reach your step counts, and complete this movement session.'],
        ['guided_relaxation', 'Today we are going to recharge the mind and soul. Come with me and learn some new relaxation skills.'],
        ['hayes', 'Dr. Michael Hayes might have some pearls of wisdom that would help you today.  Let\'s listen.']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'high',
        'pain': 'high', 'distress': 'medium',
        'intervention':
        [
        ['hayes', 'If there\'s one thing that I am sure of, it\'s the expertise of our cancer institute psychologist.  Let\'s see what he might have to say to you.'],
        ['guided_relaxation', 'Well, I\'m no expert, but I know someone who is.  How about we let the experts teach you some relaxation techniques.'],
        ['guided_relaxation', 'Today we are going to walk through one method of relaxation. Are you ready to learn?']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'medium',
        'pain': 'high', 'distress': 'medium',
        'intervention':
        [
        ['soothing_music', 'Let\'s try and leave the real world behind for a little bit. I have some nice music that will take you to a wonderful place.'],
        ['balance', 'They say moving does a body good. Let\'s test that theory out. Today I\'m asking you to reach your step counts and complete this movement session.'],
        ['strengthening', 'They say moving does a body good. Let\'s test that theory out. Today I\'m asking you to reach your step counts and complete this movement session.']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'low',
        'pain': 'high', 'distress': 'medium',
        'intervention':
        [
        ['soothing_music', 'Let\'s try and leave the real world behind for a little bit. I have some nice music that will take you to a wonderful place.'],
        ['balance', 'Getting the blood pumping makes us feel better. Are you ready to get down and get funky?  Awesome!  Walk more to reach your step counts, and complete this movement session.'],
        ['stretching', 'Getting the blood pumping makes us feel better. Are you ready to get down and get funky?  Awesome!  Walk more to reach your step counts, and complete this movement session.']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'high',
        'pain': 'medium', 'distress': 'medium',
        'intervention':
        [
        ['walking', 'Let\'s get that body moving. Are you ready?'],
        ['balance', 'Step 1.  Step more.  Step 2.  Try this movement session, designed with you in mind.  Step 3.  Pat yourself on the back.'],
        ['strengthening', 'Step 1.  Step more.  Step 2.  Try this movement session, designed with you in mind.  Step 3.  Pat yourself on the back.']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'medium',
        'pain': 'medium', 'distress': 'medium',
        'intervention':
        [
        ['balance', 'Maybe getting your blood pumping a little might make you feel better. For today, try reaching your step goal and completing this movement session'],
        ['strengthening', 'Maybe getting your blood pumping a little might make you feel better. For today, try reaching your step goal and completing this movement session'],
        ['hayes', 'Dr. Michael Hayes might have some pearls of wisdom that would help you today.  Let\'s listen.'], 
        ['balance', 'They say moving does a body good. Let\'s test that theory out. Today I\'m asking you to reach your step counts and complete this movement session.']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'low',
        'pain': 'medium', 'distress': 'medium',
        'intervention':
        [
        ['strengthening', 'They say moving does a body good. Let\'s test that theory out.  Reach or exceed your step goal, and try this movement session.'], 
        ['zucker', 'Dr David Zucker has some tips that might help you manage the symptoms you are feeling. Would you like to have a look?'], 
        ['soothing_music', 'I have just the right selection to take you to another place. I hope it makes you feel better.']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'high',
        'pain': 'low', 'distress': 'medium',
        'intervention':
        [
        ['balance', 'Let\'s get that body moving by increasing your steps and completing this movement session. Are you ready?'],
        ['strengthening', 'Raise your hand if you want to have less fatigue. You! yes you there, with the hand up. I have just the thing: increase your step counts, and try this movement session.'],
        ['walking', 'Let\'s get that body moving. Are you ready?']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'medium',
        'pain': 'low', 'distress': 'medium',
        'intervention':
        [
        ['balance', 'What\'s that?  You\'d like to run a marathon this year?  Well, maybe for now we could focus on your step goal and this movement session.  Deal?'],
        ['strengthening', 'Maybe getting your blood pumping a little might make you feel better. Can we try a movement session designed with you in mind?'], 
        ['hayes', 'If there\'s one thing that I am sure of, it\'s the expertise of our cancer institute psychologist.  Let\'s see what he might have to say to you.']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'low',
        'pain': 'low', 'distress': 'medium',
        'intervention':
        [
        ['strengthening', 'Maybe getting your blood pumping a little might make you feel better. Can we try a movement session designed with you in mind?'], 
        ['zucker', 'Dr. David Zucker helps those living with cancer see their journey in a new light.  Listen...'], 
        ['walking', 'Let\'s get that body moving. Are you ready?']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'high',
        'pain': 'high', 'distress': 'low',
        'intervention':
        [
        ['zucker', 'We are so eager to be helpful.  Please do think about ways we can help and tell us at your next weekly call.  For now, here\'s some guidance from cancer expert Dr. David Zucker.'],
        ['balance', 'Maybe getting your blood pumping a little might make you feel better. Can we try a movement session designed with you in mind?'],
        ['stretching', 'Maybe getting your blood pumping a little might make you feel better. Can we try a movement session designed with you in mind?'],
        ['guided_relaxation', 'Today we are going to recharge the mind and soul. Come with me and learn some new relaxation skills.']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'medium',
        'pain': 'high', 'distress': 'low',
        'intervention':
        [
        ['stretching', 'Maybe getting your blood pumping a little might make you feel better. Can we try a movement session designed with you in mind?'],
        ['guided_relaxation', 'Today we are going to walk through one method of relaxation. Are you ready to learn?'],
        ['balance', 'Maybe getting your blood pumping a little might make you feel better. Can we try a movement session designed with you in mind?'],
        ['guided_relaxation', 'Today we are going to recharge the mind and soul. Come with me and learn some new relaxation skills.']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'low',
        'pain': 'high', 'distress': 'low',
        'intervention':
        [
        ['stretching', 'Maybe getting your blood pumping a little might make you feel better. Can we try a movement routine designed just for you?'],
        ['guided_relaxation', 'Today we are going to recharge the mind and soul. Come with me and learn some new relaxation skills.'],
        ['balance', 'Maybe getting your blood pumping a little might make you feel better. Can we try a movement routine designed just for you?']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'high',
        'pain': 'medium', 'distress': 'low',
        'intervention':
        [
        ['balance', 'Let\'s get that body moving. Are you ready?'],
        ['strengthening', 'They say moving does a body good. Let\'s test that theory out. Today I\'m asking you to reach your step counts and complete this movement session.']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'medium',
        'pain': 'medium', 'distress': 'low',
        'intervention':
        [
        ['walking', 'Let\'s get that body moving. Are you ready?'], 
        ['balance', 'Maybe getting your blood pumping a little might make you feel better. Can we try an easy movement routine?'],
        ['strengthening', 'Maybe getting your blood pumping a little might make you feel better. Can we try an easy movement routine?']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'low',
        'pain': 'medium', 'distress': 'low',
        'intervention':
        [
        ['balance', 'Maybe getting your blood pumping a little might make you feel better. Can we try an easy movement routine?'],
        ['strengthening', 'Maybe getting your blood pumping a little might make you feel better. Can we try an easy movement routine?'], 
        ['walking', 'Maybe getting your blood pumping a little might make you feel better. Can we try an easy movement routine?'], 
        ['soothing_music', 'Soothing music is a great way to leave the world behind for awhile. Would you like to try some?']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'high',
        'pain': 'low', 'distress': 'low',
        'intervention':
        [
        ['walking', 'Getting the blood pumping makes us feel better. Are you ready to get moving today?'],
        ['strengthening', 'Maybe getting your blood pumping a little might make you feel better. Can we try an easy movement routine?'],
        ['strengthening', 'They say moving does a body good. Let\'s test that theory out. Today I\'m asking you to reach your step counts and complete this movement session.']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'medium',
        'pain': 'low', 'distress': 'low',
        'intervention':
        [
        ['walking', 'Walking is the number 1 recommendation for combatting the symptoms you are experiencing. Please look at your step goal and work toward meeting or exceeding it.  '],
        ['walking', 'Walking is the number 1 recommendation for combatting the symptoms you are experiencing. Please look at your step goal and work toward meeting or exceeding it.  '],
        ['balance', 'I am so very glad that things seem to be going well.  Let\'s keep the body going with a movement session, okay?'],
        ['strengthening', 'I am so very glad that things seem to be going well.  Let\'s keep the body going with a movement session, okay?']
        ]
    },
    {
        'sleep': 'low', 'fatigue': 'low',
        'pain': 'low', 'distress': 'low',
        'intervention':
        [
        ['walking', 'Well, based on everything we know, I think we should get you moving!'], 
        ['walking', 'Walking is the number 1 recommendation for combatting the symptoms you are experiencing. Please look at your step goal and work toward meeting or exceeding it.']
        ]
    }

]




MEDIA_TYPE = {
    'soothing_music': 'audio',
    'zucker': 'audio',
    'balance': 'video',
    'stretching': 'video',
    'strengthening': 'video',
    'hayes': 'video',
    'guided_relaxation': 'audio',
    'walking': None,
    'connect': 'webpage',
    'palliative_care': 'video',
    'movements': 'video',
    'chair_exercise': 'video', 
    'get_to_floor': 'video'
}





#the sequence of urls in each intervention's list matters!!!
MEDIA_FILE = {
    'soothing_music': 
        [
            'https://nurse-amie.s3.us-east-2.amazonaws.com/soothing_music/3+HOURS+Relaxing+Music+with+Water+Sounds+Meditation.mp3',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/soothing_music/Indian+Background+Flute+Music_+Instrumental+Meditation+Music+_+Yoga+Music+_+Spa+Music+for+Relaxation.mp3',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/soothing_music/Music+for+Healing+female+energy.mp3',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/soothing_music/8-Hours-Soothing-Music-Combined.mp3'

        ],
    'movements': 
        [
            'https://nurse-amie.s3.us-east-2.amazonaws.com/introduction/Getting+to+the+Floor_FINAL_04-13-17.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/balance/Level+1+No+Mets+Balance+FINAL_04-13-17.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/strength/Level+1+No+Mets+Strength_FINAL_04-13-17.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/stretching/Level+1+No+Mets+Stretching_FINAL_04-13-17.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/balance/Level+2+No+METS+Balance_FINAL_04-17-17.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/strength/Level+2+No+METS+Strength_FINAL_04-13-17.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/stretching/Level+2+No+METS+Stretching_FINAL_04-13-17.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/balance/Level+3+No+METS+Balance_FINAL_04-17-17.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/strength/Level+3+No+METS+Strength_FINAL_04-13-17.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/stretching/Level+3+No+METS+Stretching_FINAL_04-13-17.mp4'
        ],
    'zucker': 
        [
            'https://nurse-amie.s3.us-east-2.amazonaws.com/zucker/1_imagining+future+dissolved.mp3',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/zucker/2_100+trillion+healthy+cells.mp3',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/zucker/3_tx+related+fatigue.mp3',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/zucker/4_dont+fall+thorugh+the+ice.mp3',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/zucker/5_managing+fatigue.mp3',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/zucker/6_many+fitness+levels+one+you.mp3',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/zucker/7_too+much+of+a+good+thing+is+a+bad+thing.mp3',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/zucker/8_check+the+tires+before+the+road+trip.mp3',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/zucker/9_metabolic+stewardship.mp3'
        ],
    'balance':
        {
           'no met': {
                        '1': 'https://nurse-amie.s3.us-east-2.amazonaws.com/balance/Level+1+No+Mets+Balance+FINAL_04-13-17.mp4',
                        '2': 'https://nurse-amie.s3.us-east-2.amazonaws.com/balance/Level+2+No+METS+Balance_FINAL_04-17-17.mp4',
                        '3': 'https://nurse-amie.s3.us-east-2.amazonaws.com/balance/Level+3+No+METS+Balance_FINAL_04-13-17.mp4'
                    },
            'upper body': {
                        '1': 'https://nurse-amie.s3.us-east-2.amazonaws.com/balance/Level+1+Upper+Body+METS+Balance_FINAL_04-13-17.mp4',
                        '2': 'https://nurse-amie.s3.us-east-2.amazonaws.com/balance/Level+2+Upper+Body+Mets+Balance_FINAL_04-13-17.mp4',
                        '3': 'https://nurse-amie.s3.us-east-2.amazonaws.com/balance/Level+3+Upper+Body+METS+Balance_FINAL_04-13-17.mp4'
                    },
            'torso':{
                        '1': 'https://nurse-amie.s3.us-east-2.amazonaws.com/balance/Level+1+Torso+METS+Balance_FINAL_04-13-17.mp4',
                        '2': 'https://nurse-amie.s3.us-east-2.amazonaws.com/balance/Level+2+Torso+METS+Balance_FINAL_04-13-17.mp4',
                        '3': 'https://nurse-amie.s3.us-east-2.amazonaws.com/balance/Level+3+Torso+METS+Balance_FINAL_04-13-17.mp4'
            }
        },
    'hayes': 
        [
            'https://nurse-amie.s3.us-east-2.amazonaws.com/hayes/Introduction+to+DBT.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/hayes/DBT+Mindfulness.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/hayes/DBT+Wise+Mind.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/hayes/DBT+Interpersonal+Effectiveness+Skills.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/hayes/DBT+Emotional+Regulation.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/hayes/DBT+Radical+Acceptance+Skills.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/hayes/Understanding+Anxiety.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/hayes/Anxiety+Part+2.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/hayes/Anxiety+Part+3.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/hayes/Understanding+Depression.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/hayes/Toolbox.mp4'
        ],
    'stretching': 
        {
           'no met': {
                        '1': 'https://nurse-amie.s3.us-east-2.amazonaws.com/stretching/Level+1+No+Mets+Stretching_FINAL_04-13-17.mp4',
                        '2': 'https://nurse-amie.s3.us-east-2.amazonaws.com/stretching/Level+2+No+METS+Stretching_FINAL_04-13-17.mp4',
                        '3': 'https://nurse-amie.s3.us-east-2.amazonaws.com/stretching/Level+3+No+METS+Stretching_FINAL_04-13-17.mp4'
                    },
            'upper body': {
                        '1': 'https://nurse-amie.s3.us-east-2.amazonaws.com/stretching/Level+1+Upper+Body+METS+Stretching_FINAL_04-13-17.mp4',
                        '2': 'https://nurse-amie.s3.us-east-2.amazonaws.com/stretching/Level+2+Upper+Body+METS+Stretching_FINAL_04-13-17.mp4',
                        '3': 'https://nurse-amie.s3.us-east-2.amazonaws.com/stretching/Level+3+Upper+Body+METS+Stretching_FINAL_04-13-17.mp4'
                    },
            'torso':{
                        '1': 'https://nurse-amie.s3.us-east-2.amazonaws.com/stretching/Level+1+Torso+METS+Stretching+Final+04-13-17.mp4',
                        '2': 'https://nurse-amie.s3.us-east-2.amazonaws.com/stretching/Level+2+Torso+METS+Stretching_FINAL_04-13-17.mp4',
                        '3': 'https://nurse-amie.s3.us-east-2.amazonaws.com/stretching/Level+3+Torso+METS+Stretching_FINAL_04-13-17.mp4'
            }
        },
    'palliative_care':
        [
            'https://nurse-amie.s3.us-east-2.amazonaws.com/palliative_care/Palliative+Care_+YOU+Are+a+BRIDGE.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/palliative_care/Introduction+to+Palliative+Care.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/palliative_care/Palliative+Care_Pain+and+Neuropathy.mp4',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/palliative_care/Palliative+Care_Wellness.mp4'
        ],
    'guided_relaxation':
        [
            'https://nurse-amie.s3.us-east-2.amazonaws.com/guided_relaxation/aob.mp3',
            'https://nurse-amie.s3.us-east-2.amazonaws.com/guided_relaxation/bringing-the-breath-into-everyday-life.mp3', 
            'https://nurse-amie.s3.us-east-2.amazonaws.com/guided_relaxation/whole-body-awareness.mp3'
        ],
    'strengthening': 
            {
           'no met': {
                        '1': 'https://nurse-amie.s3.us-east-2.amazonaws.com/strength/Level+1+No+Mets+Strength_FINAL_04-13-17.mp4',
                        '2': 'https://nurse-amie.s3.us-east-2.amazonaws.com/strength/Level+2+No+METS+Strength_FINAL_04-13-17.mp4',
                        '3': 'https://nurse-amie.s3.us-east-2.amazonaws.com/strength/Level+3+No+METS+Strength_FINAL_04-13-17.mp4'
                    },
            'upper body': {
                        '1': 'https://nurse-amie.s3.us-east-2.amazonaws.com/strength/Level+1+Upper+Body+METS+Strength_FINAL_04-13-17.mp4',
                        '2': 'https://nurse-amie.s3.us-east-2.amazonaws.com/strength/Level+2+Upper+Body+METS+Strength_FINAL_04-13-17.mp4',
                        '3': 'https://nurse-amie.s3.us-east-2.amazonaws.com/strength/Level+3+Upper+Body+METS+Strength_FINAL_04-13-17.mp4'
                    },
            'torso':{
                        '1': 'https://nurse-amie.s3.us-east-2.amazonaws.com/strength/Level+1+Torso+METS+Strength_FINAL_04-13-17.mp4',
                        '2': 'https://nurse-amie.s3.us-east-2.amazonaws.com/strength/Level+2+Torso+METS+Strength_FINAL_04-13-17.mp4',
                        '3': 'https://nurse-amie.s3.us-east-2.amazonaws.com/strength/Level+3+Torso+METS+Strength_FINAL_04-13-17.mp4'
            }
        },
    'connect': 
        [
            'https://www.breastcancer.org'
        ],
    'walking':
        [
            None
        ],
    'chair_exercise': 
        [
            'https://nurse-amie.s3.us-east-2.amazonaws.com/chair_exercise/Chair+Workout+FINAL_04-13-17.mp4'
        ],
    'get_to_floor':
        [
            'https://nurse-amie.s3.us-east-2.amazonaws.com/introduction/Getting+to+the+Floor_FINAL_04-13-17.mp4'
        ]
}




MEDIA_FILE_TITLE = {
    'soothing_music': 
        [
            '3 HOURS Relaxing Music with Water Sounds Meditation',
            'Indian Background Flute Music Instrumental Meditation Music Yoga Music Spa Music for Relaxation',
            'Music for Healing female energy',
            '8 Hours Soothing Music Combined'

        ],
    'movements': 
        [
            'introduction Getting to the Floor',
            'Level 1 No Mets Balance',
            'Level 1 No Mets Strength',
            'Level 1 No Mets Stretching',
            'Level 2 No METS Balance',
            'Level 2 No METS Strength',
            'Level 2 No METS Stretching',
            'Level 3 No METS Balance',
            'Level 3 No METS Strength',
            'Level 3 No METS Stretching'
        ],
    'zucker': 
        [
            '1 imagining future dissolved',
            '2 100 trillion healthy cells',
            '3 tx related fatigue',
            '4 dont fall thorugh the ice',
            '5 managing fatigue',
            '6 many fitness levels one you',
            '7 too much of a good thing is a bad thing',
            '8 check the tires before the road trip',
            '9 metabolic stewardship'
        ],
    'balance':
        [
            'Level 1 No Mets Balance',
            'Level 1 Torso METS Balance',
            'Level 1 Upper Body METS Balance',
            'Level 2 No METS Balance',
            'Level 2 Torso METS Balance',
            'Level 2 Upper Body Mets Balance',
            'Level 3 No METS Balance',
            'Level 3 Torso METS Balance',
            'Level 3 Upper Body METS Balance'
        ],
    'hayes': 
        [
            'Introduction to DBT',
            'DBT Mindfulness',
            'DBT Wise Mind',
            'DBT Interpersonal Effectiveness Skills',
            'DBT Emotional Regulation',
            'DBT Radical Acceptance Skills',
            'Understanding Anxiety',
            'Anxiety Part 2',
            'Anxiety Part 3',
            'Understanding Depression',
            'Toolbox'
        ],
    'stretching': 
        [
            'Level 1 No Mets Stretching',
            'Level 1 Torso METS Stretching Final',
            'Level 1 Upper Body METS Stretching',
            'Level 2 No METS Stretching',
            'Level 2 Torso METS Stretching',
            'Level 2 Upper Body METS Stretching',
            'Level 3 No METS Stretching',
            'Level 3 Torso METS Stretching',
            'Level 3 Upper Body METS Stretching'

        ],
    'palliative_care':
        [
            'Palliative Care YOU Are a BRIDGE',
            'Introduction to Palliative Care',
            'Palliative Care_Pain and Neuropathy',
            'Palliative Care_Wellness'
        ],
    'guided_relaxation':
        [
            'aob',
            'bringing the breath into everyda life', 
            'whole body awareness'
        ],
    'strengthening': 
        [
            'Level 1 No Mets Strength',
            'Level 1 Torso METS Strength',
            'Level 1 Upper Body METS Strength',
            'Level 2 No METS Strength',
            'Level 2 Torso METS Strength',
            'Level 2 Upper Body METS Strength',
            'Level 3 No METS Strength',
            'Level 3 Torso METS Strength',
            'Level 3 Upper Body METS Strength'
        ],
    'connect': 
        [
            'https://www.breastcancer.org'
        ],
    'walking':
        [
            None
        ]
}