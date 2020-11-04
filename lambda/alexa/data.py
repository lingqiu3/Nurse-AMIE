

########################   Voice  ##################################

ASK_ACCOUNT_LINKING_VOICE = ('<amazon:emotion name="excited" intensity="low">Hello! Welcome to Nurse AMIE. I will be '
                        'your personal assistant, helping you with '
                        'your breast cancer. Since this is our first meeting, could you please go to the Alexa app to link your Amazon account '
                        'with Nurse AMIE? I will see you around!</amazon:emotion>')


WELCOME_FIRST_TIME_VOICE = ('<amazon:emotion name="excited" intensity="low">Welcome, {}!'
                    'My name is Amie and I am going to help you navigate the resources available to you. I hope that you find these resources helpful. '
                    '<break time="1s"/> </amazon:emotion> Before we get started, let me collect some health information from you. '
                    'Do you have bone metastases? You can answer yes or no.')

'''
WELCOME_FIRST_TIME_VOICE = ('<amazon:emotion name="excited" intensity="low">Welcome, {}! Let\'s get started!'
                    'Since you are a first time user, you must be wondering who is nurse amie. Is she real? You can say yes to '
                                'solve your doubt or say no to skip it.</amazon:emotion>')
'''

INTRODUCTION_VIDEO_VOICE = ("Let me show a video to introduce Nurse AMIE.")

USER_LOGIN_SAME_DAY_VOICE = ("Back so soon? We are not scheduled to talk again until tomorrow")

SLOT_ASK_VOICE ={
        'sleep': 'How would you rate your sleep?',
        'fatigue': 'How would you rate your fatigue?',
        'distress': 'How would you rate your distress?',
        'pain': 'How would you rate your pain?',
        'steps': 'One last thing, how many steps did you record on your pedometer since yesterday?'
    }
    
PROMPT_CHANGE_GUIDED_SLOT_VOICE = ("What are the symptom levels you would like to change?")

REPROMPT_CHANGE_GUIDED_SLOT_VOICE = ("For example, you can say sleep and distress.")

CHANGE_SLOT_ASK_VOICE ={
        'sleep': 'How would you rate your sleep?',
        'fatigue': 'How would you rate your fatigue?',
        'distress': 'How would you rate your distress?',
        'pain': 'How would you rate your pain?', 
        'steps': 'How many steps did you record on your pedometer since yesterday?'
    }

CONFIRM_GUIDED_SLOT_VOICE = ('This is your today\'s health condition summary. '
                            'You can say YES to start the recommended activity or '
                            'say NO to revise this information.')

ASK_USER_START_INTERVENTION = ('Are you ready to start today\'s activity?')

ASK_USER_START_VIDEO_INTERVENTION_MEDIA = ('If you are ready, please say play video.')

ASK_USER_START_AUDIO_INTERVENTION_MEDIA = ('If you are ready, please say play audio.')

ASK_USER_GET_TO_FLOOR_FIRST = ('To get you ready for the exercise. please play the first video, Get To Floor, '
                                'Then please proceed to the second video, which leads to your today\'s intervention activity. ' 
                                'To start the first video, you can either say \' play get to floor\' or select it on the screen. ' )

ASK_USER_START_SYMPTOM_QUESTIONS = ('Welcome Back! If you would like to continue with today\'s intervention activity, say start intervention!')

ASK_USER_REVIEW_INTERVENTION = ('Hey, we have already met today! Would you like to review today\'s intervention activity?')

GET_TO_FLOOR_VOICE = ("Before we get started, let me show you some preliminary information about exercising.")

HALFWAY_EXIT_VOICE = ("Sorry to hear that you are about to leave. Hope I can see you again today!")
EXIT_VOICE = ("See you tomorrow!")
                            
#START_GUIDED_ACTIVITY_VOICE = ('<amazon:emotion name="excited" intensity="low">Sounds Good!</amazon:emotion>')
                 

########################   APL  ##################################


WELCOME_DOCUMENT = ("./apl/welcome_page.json")
WELCOME_DOCUMENT_TOKEN = ("welcome_page")

REQUEST_SYMPTOM_LEVEL_TOKEN = ("request_symptom_level_page")
REQUEST_SYMPTOM_LEVEL_DOCUMENT = ('./apl/guided_slot.json')

CONFIRM_GUIDED_SLOT_TOKEN = ('confirm_guided_slot')
CONFIRM_GUIDED_SLOT_DOCUMENT = ('./apl/confirm_guided_slot.json')

INTRO_VIDEO_TOKEN = ('intro_video')
INTRO_VIDEO_DOCUMENT = ('./apl/nurse_amie_intro_video.json')

GET_TO_FLOOR_TOKEN = ('get_to_floor')
GET_TO_FLOOR_DOCUMENT = ('./apl/get_to_floor_video.json')

PLAY_VIDEO_DOCUMENT = ('./apl/play_video_3.json')

REQUEST_PLAY_VIDEO_INTERVENTION_DOCUMENT = ('./apl/intervention_request_play_video.json')
REQUEST_PLAY_VIDEO_INTERVENTION_TOKEN = ('request_play_video_intervention')

REQUEST_PLAY_AUDIO_INTERVENTION_DOCUMENT = ('./apl/intervention_request_play_audio.json')
REQUEST_PLAY_AUDIO_INTERVENTION_TOKEN = ('request_play_audio_intervention')

REQUEST_PLAY_GET_TO_FLOOR_DOCUMENT = ('./apl/intervention_request_play_get_to_floor.json')
REQUEST_PLAY_GET_TO_FLOOR_TOKEN = ('request_play_get_to_floor_intervention')

EXIT_TOKEN = ('exit_nurse_amie')
EXIT_DOCUMENT = ('./apl/exit_nurse_amie.json')

PINK_RIBBON_DOCUMENT = ("./apl/pink_ribbon_menu.json")
PINK_RIBBON_TOKEN = ("pink_ribbon_menu")

MOVEMENT_LIST_TOKEN = ("movements_list")
MOVEMENT_LIST_NO_MET_DOCUMENT = ("./apl/movements_no_met_list.json")
MOVEMENT_LIST_UPPER_BODY_DOCUMENT = ("./apl/movements_upper_body_list.json")
MOVEMENT_LIST_LOWER_BODY_DOCUMENT = ("./apl/movements_lower_body_list.json")
MOVEMENT_LIST_TORSO_DOCUMENT = ("./apl/movements_torso_list.json")

GUIDED_RELAXATION_LIST_DOCUMENT = ("./apl/guided_relaxation_list.json")
GUIDED_RELAXATION_LIST_TOKEN = ("guided_relaxation_list")

SOOTHING_MUSIC_LIST_DOCUMENT = ("./apl/soothing_music_list.json")
SOOTHING_MUSIC_LIST_TOKEN = ("soothing_music_list")

COPING_SYMPTOMS_LIST_DOCUMENT = ("./apl/coping_symptoms_list.json")
COPING_SYMPTOMS_LIST_TOKEN = ("coping_symptoms_list")

NUTRITION_HOMEPAGE_DOCUMENT = ("./apl/nutrition_homepage.json")
NUTRITION_HOMEPAGE_TOKEN = ("nutrition_homepage")

NUTRITION_FAVOURITE_LIST_DOCUMENT = ("./apl/favourite_nutrition_list.json")
NUTRITION_FAVOURITE_LIST_TOKEN = ("favourite_nutrition_list")

RECIPE_CATEGORY_DOCUMENT = ("./apl/recipe_category.json")
RECIPE_CATEGORY_TOKEN = ("recipe_category")

RECIPE_CATEGORY_LIST_DOCUMENT = ("./apl/recipe_category_list.json")
RECIPE_CATEGORY_LIST_TOKEN = ("recipe_category_list")

NUTRITION_RECIPE_INTO_DOCUMENT = ("./apl/recipe_intro.json")
NUTRITION_FAVOURITE_RECIPE_INTRO_TOKEN = ("favourite_nutrition_item")
NUTRITION_NEW_RECIPE_INTRO_TOKEN = ("new_nutrition_item")
NUTRITION_CATEGORY_RECIPE_INTRO_TOKEN = ("category_nutrition_item")

NUTRITION_TOPIC_OF_DAY_DOCUMENT = ("./apl/nutrition_topic_of_day.json")
NUTRITION_TOPIC_OF_DAY_TOKEN = ("nutrition_topic_of_day")

NUTRITION_TOPIC_OF_DAY_NO_SPEAKITEM_DOCUMENT = ("./apl/nutrition_topic_of_day_no_speakitem.json")
NUTRITION_TOPIC_OF_DAY_NO_SPEAKITEM_TOKEN = ("nutrition_topic_of_day_no_speakitem")



#####################  data   ####################################
GUIDED_SLOT_SYMPTOM = ['sleep', 'fatigue', 'distress', 'pain']
GUIDED_SLOT = ['sleep', 'fatigue', 'distress', 'pain', 'steps']

SYMPTOM_LEVEL_APL_DATASOURCES = {
    'sleep': {'LambdaData': 
        {'RenderText': 'sleep', 
        'Background': 'https://apldmo.s3.amazonaws.com/symptom_level_background.jpg',
        'HintText1': 'Response a number from 0 to 10'
        }},
    'fatigue': {'LambdaData': 
        {'RenderText': 'fatigue', 
        'Background': 'https://apldmo.s3.amazonaws.com/symptom_level_background.jpg',
        'HintText1': 'Response a number from 0 to 10'
        }},
    'distress': {'LambdaData': 
        {'RenderText': 'distress', 
        'Background': 'https://apldmo.s3.amazonaws.com/symptom_level_background.jpg',
        'HintText1': 'Response a number from 0 to 10'
        }},
    'pain': {'LambdaData': 
        {'RenderText': 'pain', 
        'Background': 'https://apldmo.s3.amazonaws.com/symptom_level_background.jpg',
        'HintText1': 'Response a number from 0 to 10'
        }},
    'steps': {'LambdaData': 
        {'RenderText': 'steps', 
        'Background': 'https://apldmo.s3.amazonaws.com/raw_background.jpg',
        'HintText1': 'Response with a number'
        }}
}

#####################  Welcome Voice   ####################################
WELCOME_VOICE = [
    "G’day! How ya doing?",
    "Hello! Hope I can help. What’s happening with you?",
    "Hi. Here I am. There you are. Let’s start.",
    "So nice to have you back!",
    "Whoops, hold on, nearly ready! . . . ah, there we are.",
    "And, we’re off!",
    "So nice to see you. Let’s get started.",
    "Back again? Wonderful!",
    "Well, hey there!"
]

########## Dashboard ######
DASH_BOARD_POST_URL = ""  # needs to be changed
