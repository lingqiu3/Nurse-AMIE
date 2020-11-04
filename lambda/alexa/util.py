from . import data, media_data, nutrition_data
import six
import json
import boto3
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.slu.entityresolution import StatusCode
from ask_sdk_model.dialog import (
    ElicitSlotDirective, DelegateDirective)
from ask_sdk_model.interfaces.alexa.presentation.apl import (
    RenderDocumentDirective, AnimatedOpacityProperty, AnimateItemCommand,
    ExecuteCommandsDirective, UserEvent, OpenUrlCommand, ControlMediaCommand,
    SpeakItemCommand, HighlightMode)
from ask_sdk_model import (Response, Slot, Intent, DialogState)
from ask_sdk_core.utils import is_intent_name, get_account_linking_access_token
from ask_sdk_model.interfaces.videoapp import (LaunchDirective, VideoAppInterface, VideoItem)
from ask_sdk_model.interfaces.audioplayer import (PlayDirective, AudioItem, Stream, AudioItemMetadata, PlayBehavior, StopDirective)
from datetime import datetime 
from boto3.dynamodb.conditions import Key
import requests
import random
import logging
# to host external python packages on AWS
# pip3 install pytz -t . 
import pytz

logger = logging.getLogger(__name__)

def load_apl_document(file_path):
    # type: (str) -> Dict[str, Any]
    """Load the apl json document at the path into a dict object."""
    with open(file_path) as f:
        return json.load(f)
        

def get_welcome_voice():
    """Return state information in well formatted text."""
    speak_output = random.choice(data.WELCOME_VOICE) + \
                ' Do you think yesterday\'s activity is useful?'
    return speak_output

def get_welcome_first_time_voice(name):
    """Return state information in well formatted text."""
    return data.WELCOME_FIRST_TIME_VOICE.format(name)
        


def check_first_time_user(user_id):
    # check if the user first time uses Nurse AMIE, 
    # i.e. if her UserID is found in the DynamoDB database: Nurse_AMIE_User_Progress_Status
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Nurse_AMIE_User_Progress_Status')
    response = table.query(
        KeyConditionExpression=Key('UserID').eq(user_id))
    if response['Count'] == 0:
        return True
    else:
        return False

    

def need_to_ask_intervention_feedback(user_email):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Nurse_AMIE_User_Skill_State')
    response = table.query(
        KeyConditionExpression = Key('UserID').eq(user_email))
    if response['Count'] == 0:
        return False
    else:
        if response['Items'][0]['State'] == "intervention_activity_initated":
            return True
        else:
            return False


def log_intent_activity_DB(handler_input, session_attr, intent_name):
    # either directly trigger the intent or tiggered by PreviousIntent
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Nurse_AMIE_User_Activity_Log')
    if (is_intent_name(intent_name)(handler_input) or 
        is_intent_name("AMAZON.PreviousIntent")(handler_input)):
        user_activity_log = {'Activity':  intent_name, 'Status': 'voice'}
    else:
        user_activity_log = {'Activity':  intent_name, 'Status': 'touch'}
    if 'user_email' in session_attr:
        write_user_data_to_DynamoDB(table, session_attr['user_email'], user_activity_log, log_timestamp=True)
    else:
        access_token = get_account_linking_access_token(handler_input)
        user_email = get_user_profile(access_token, user_info = 'email')
        write_user_data_to_DynamoDB(table, session_attr['user_email'], user_activity_log, log_timestamp=True)

    
def ask_guided_activity_slot(slot, voice_list):
    for key in voice_list:
        if slot == key:
            return voice_list[key]



def not_match_guided_slot_match(slots, slot_var, session_attr):
    if (slot_var in session_attr):
        # 'steps' type is Amazon.Numbers, therefore, can not use ER_SUCCESS_MATCH on 'steps'
        if (slot_var == 'steps'):
            return False
        if (slots[slot_var].resolutions):
            if (slots[slot_var].resolutions.resolutions_per_authority[0].status.code != StatusCode.ER_SUCCESS_MATCH):
                return True
        else:
            return True
    else:
        return True
    return False
    
def er_success_match(slot, slot_value=None):
    if (slot.resolutions):
        print (slot.resolutions.resolutions_per_authority[0])
        if (slot.resolutions.resolutions_per_authority[0].status.code == StatusCode.ER_SUCCESS_MATCH):
            print ('all good here')
            if (slot_value == None):
                return True
            else:
                if (slot.resolutions.resolutions_per_authority[0].values[0].value.name == slot_value):
                    return True
                else:
                    return False
    return False



def log_slot_resolutions_value(slot):
    return slot.resolutions.resolutions_per_authority[0].values[0].value.name
  

def render_screen(response_builder, token, document, datasources=None):
    response_builder.add_directive(
        RenderDocumentDirective(
            token = token,
            document = load_apl_document(document),
            datasources = datasources))
    return response_builder

def elicit_slot(response_builder, slot_to_elicit, next_intent=None):
    response_builder.add_directive(
        ElicitSlotDirective(
            updated_intent=next_intent, 
            slot_to_elicit=slot_to_elicit))
    return response_builder


def delegate_intent(response_builder, intent):
    response_builder.add_directive(
            directive=DelegateDirective(updated_intent=Intent(
            name=intent)))
    return response_builder



def log_user_intervention_feedback(user_id, intervention_activity, intervention_feedback, exercise_level_feedback = None):
    dynamodb = boto3.resource('dynamodb')
    intervention_activity = ','.join(intervention_activity)
    user_data = {'intervention': intervention_activity, 'intervention_feedback': intervention_feedback}
    # write exercise feedback if needed
    if exercise_level_feedback != None:
        user_data['exercise_feedback'] = exercise_level_feedback
    write_user_data_to_DynamoDB(table = dynamodb.Table('Nurse_AMIE_User_Intervention_Feedback'), 
                            user_id = user_id, 
                            user_data = user_data, 
                            log_timestamp = True)


def update_user_exercise_level(user_id, exercise_level_feedback):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Nurse_AMIE_User_Progress_Status')
    response = table.query(
        KeyConditionExpression = Key('UserID').eq(user_id) & Key('Activity').eq('exercise_level'))
    current_exercise_level = int(response['Items'][0]['Status'])
    user_data = {'Activity': 'exercise_level'}
    if exercise_level_feedback == 'too easy' and current_exercise_level < 3:
        user_data['Status'] = str(current_exercise_level+1)
        speak_output = 'Ok, I will level up your exercise a little bit. '
    elif exercise_level_feedback == 'too hard' and current_exercise_level > 1:
        user_data['Status'] = str(current_exercise_level-1)
        speak_output = 'Ok, I will make your exercie a bit easier. '
    else:
        user_data['Status'] = str(current_exercise_level)
        speak_output = 'Thank you for letting me know. '
    write_user_data_to_DynamoDB(table = table, 
                            user_id = user_id, 
                            user_data = user_data)
    return speak_output

def log_user_symptom_level(session_attr):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Nurse_AMIE_User_Symptom_Status')
    user_data = collect_symptom_data_from_sessionattr(session_attr)
    # log the symptom level regarding exercise
    if (((session_attr['intervention_category'] == 'balance') or 
        (session_attr['intervention_category'] == 'stretching') or 
        (session_attr['intervention_category'] == 'strengthening'))):
        user_data['intervention'] = (session_attr['intervention_category'] + ',' + 
                                    session_attr['met_location'] + ',' + session_attr['exercise_level'])
    else:
        user_data['intervention'] = session_attr['intervention_category']+ ',' + str(session_attr['intervention_progress'])
    write_user_data_to_DynamoDB(table = dynamodb.Table('Nurse_AMIE_User_Symptom_Status'), 
                            user_id = session_attr['user_email'], 
                            user_data = user_data, 
                            log_timestamp = True)



def collect_symptom_data_from_sessionattr(session_attr):
    symptom_level_summary = {}
    for symptom in data.GUIDED_SLOT:
        symptom_level_summary[symptom] = int(session_attr[symptom+'_value'])
    #symptom_level_summary['contact_clinical_team'] = session_attr['contact_clinical_team']
    return symptom_level_summary
        



def write_user_data_to_DynamoDB(table, user_id, user_data, log_timestamp=False):
    item = {
        'UserID': user_id
    }
    if log_timestamp == True:
        item['Datetime'] = int(datetime.timestamp(datetime.now()))
    #add user data to item
    for i in user_data: item[i] = user_data[i]
    table.put_item(
        Item=item)

def put_item_DynamoDB_UserID_Activity(table, user_id, user_data):
    item = {
        'UserID': user_id
    }
    #add user data to item
    for i in user_data: item[i] = user_data[i]
    table.put_item(
        Item=item)


''' Example

{'UserId': 'lingqiu33@outlook.com', 
'Questions': [{'type': 'sleep', 'value': '5'}, 
              {'type': 'fatigue', 'value': '4'}, 
              {'type': 'distress', 'value': '3'}, 
              {'type': 'pain', 'value': '2'}, 
              {'type': 'steps', 'value': '300'}], 
'InterventionType:': 'strengthening', 
'Intervention': 'Level 3 No METS Strength', 
'InTime': 1600392606}

'''
def send_data_external_api(session_attr):
    user_data = {
        'UserId': session_attr['user_email'],
        'Questions': [
            {'type': 'sleep', 'value': session_attr['sleep_value']},
            {'type': 'fatigue', 'value': session_attr['fatigue_value']},
            {'type': 'distress', 'value': session_attr['distress_value']},
            {'type': 'pain', 'value': session_attr['pain_value']},
            {'type': 'steps', 'value': session_attr['steps_value']}
        ],
        'InterventionType:': session_attr['intervention_category'],
        'Intervention': session_attr['intervention_title'],
        'InTime': session_attr['login_time']
    }

    # should not throw any error
    try:
        r = requests.post(data.DASH_BOARD_POST_URL, json=user_data)
        r.raise_for_status()
    except requests.exceptions.RequestException:
        logger.exception("Unable to upload data to the dashboard")


def log_skill_state_DynamoDB(user_id, skill_state):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Nurse_AMIE_User_Skill_State')
    user_activity_log = {'Datetime': int(datetime.timestamp(datetime.now())), 'State': skill_state}
    write_user_data_to_DynamoDB(table = dynamodb.Table('Nurse_AMIE_User_Skill_State'), 
                            user_id = user_id, 
                            user_data = user_activity_log, 
                            log_timestamp=True)


def log_user_activity_DB(user_id, user_activity_log):
    dynamodb = boto3.resource('dynamodb')
    write_user_data_to_DynamoDB(table = dynamodb.Table('Nurse_AMIE_User_Activity_Log'), 
                            user_id = user_id, 
                            user_data = user_activity_log, 
                            log_timestamp=True)




def create_recipe_category_datasource(user_nutrition_progress):
    recipe_category = []
    for recipe in nutrition_data.RECIPE_SCHEDULE[:user_nutrition_progress+1]:
        recipe_category += recipe['category']
    recipe_category = list(set(recipe_category))
    recipe_category_apl = []
    for category in recipe_category:
        recipe_category_apl.append({
                            "type": "SelectionTab",
                            "left": "50vw",
                            "primaryText": category,
                            "arguments": ['open_target_category', category],
                            "spacing": "3vw"
                            })
    return {
        'LambdaData': {
            'type': 'object',
            'properties': {
                'recipe_category': recipe_category_apl,
            }
        }
    }

def create_symptom_level_confirmation_datasource(session_attr):
    return {
        'LambdaData': {
            'sleep': session_attr['sleep'],
            'fatigue': session_attr['fatigue'],
            'distress': session_attr['distress'],
            'pain': session_attr['pain'],
            'steps': session_attr['steps']
            }
        }

def create_target_category_list_datasource(category_name, user_nutrition_progress):
    recipe_list = []
    for recipe in nutrition_data.RECIPE_SCHEDULE[:user_nutrition_progress+1]:
        if category_name in recipe['category']: 
            recipe_list.append({'recipe_title': recipe['title'], 'recipe_id': recipe['id']})
    return create_recipe_list_datasource(recipe_list, category_name)



def create_bookmarked_list_datasource(user_email):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Nurse_AMIE_User_Nutrition_Bookmark')
    response = table.query(
        KeyConditionExpression = Key('UserID').eq(user_email))
    user_bookmarked_recipe = []
    APL_title = "Favourite Recipes"
    if (response['Count'] == 0):
        return create_recipe_list_datasource(user_bookmarked_recipe, APL_title)
    else:
        for DB_row in response['Items']: 
            user_bookmarked_recipe.append({'recipe_title': DB_row['RecipeTitle'], 'recipe_id': DB_row['RecipeID']})
        return create_recipe_list_datasource(user_bookmarked_recipe, APL_title)

def create_recipe_list_datasource(recipe_list, APL_title):
    recipe_list_apl = []
    for recipe in recipe_list:
        recipe_list_apl.append({
                            "type": "SelectionTab",
                            "left": "50vw",
                            "primaryText": recipe['recipe_title'],
                            "arguments": ['open_recipe_intro', recipe['recipe_id']],
                            "spacing": "3vw"
                            })
    return {
        'LambdaData': {
            'type': 'object',
            'properties': {
                'recipe_list': recipe_list_apl,
                'title': APL_title
            }
        }
    }


def find_recipe(recipe_id=None):
    for recipe in nutrition_data.RECIPE_SCHEDULE:
        if recipe['id'] == recipe_id:
            return recipe



def create_topic_of_day_datasource(user_nutrition_progress):
    topic_of_day = nutrition_data.TOPIC_OF_DAY_SCHEDULE[user_nutrition_progress]
    return {
    'LambdaData': {
        'type': 'object',
        'properties': {
            'title': topic_of_day['title'],
            'subtitle': topic_of_day['subtitle'],
            'text': topic_of_day['text'],
            'text_ssml': "<speak>{}</speak>".format(topic_of_day['text']),
            'if_link': topic_of_day['if_link']
            },
            'transformers': [
                {
                    'inputPath': 'text_ssml',
                    'transformer': 'ssmlToSpeech',
                    'outputName': 'text_speech'
                }
            ]
        }
    }

def create_topic_of_day_speak(user_nutrition_progress):
    topic_of_day = nutrition_data.TOPIC_OF_DAY_SCHEDULE[user_nutrition_progress]
    if topic_of_day['title'] == 'Topic of the Day':
        speak_output = "Today's topic is " + topic_of_day['subtitle']
    else:
        speak_output = "This week's theme is " + topic_of_day['subtitle']
    return speak_output


def create_recipe_summary_datasource(recipe_data):
    recipe_category_APL = [{"primaryText": category} for category in recipe_data['category']]
    return {
    'LambdaData': {
        'type': 'object',
        'properties': {
            'recipe_title': recipe_data['title'],
            'recipe_nutrition': recipe_data['recipe_nutrition'],
            'recipe_category': recipe_category_APL
            }
        }
    }


def read_text_apl(response_builder, token, component_id): 
    response_builder.add_directive(
        ExecuteCommandsDirective(
            token=token,
            commands=[
                SpeakItemCommand(
                component_id=component_id,
                highlight_mode=HighlightMode.line)]))
    return response_builder



def addRecipeToBookmark(user_id, recipe_title, recipe_id):
    dynamodb = boto3.resource('dynamodb')
    user_data = {'RecipeTitle': recipe_title,'RecipeID': recipe_id}
    write_user_data_to_DynamoDB(table = dynamodb.Table('Nurse_AMIE_User_Nutrition_Bookmark'),
                            user_id = user_id,
                            user_data = user_data)


def generateInterventionContent(session_attr):
    for item in media_data.DECISION_TREE:
        selected = True
        for slot in data.GUIDED_SLOT_SYMPTOM:
            if item[slot] != session_attr[slot]:
                selected = False
        if selected == True:
            break
    intervention = random.choice(item['intervention'])
    intervention_category = intervention[0]
    intervention_intro_speech = intervention[1]
    return intervention_category, intervention_intro_speech


def retrieve_same_day_skill_state(user_email):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Nurse_AMIE_User_Skill_State')
    response = table.query(
        KeyConditionExpression = Key('UserID').eq(user_email))
    if response['Count'] == 0:
        return None
    else:
        if check_login_same_day(int(response['Items'][-1]['Datetime'])):
            return response['Items'][-1]['State']
        return None

def retrieve_user_intervention_activity(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Nurse_AMIE_User_Symptom_Status')
    response = table.query(
        KeyConditionExpression = Key('UserID').eq(user_id))
    intervention = response['Items'][-1]['intervention'].split(',')
    return intervention


def get_intervention_url(intervention_info_sum):
    # interventions belonging to exercise
    if len(intervention_info_sum) == 3:
        intervention_category = intervention_info_sum[0]
        metastases_location = intervention_info_sum[1]
        if metastases_location == 'lower body':
            source = media_data.MEDIA_FILE['chair_exercise'][0]
        else:
            exercise_level = intervention_info_sum[2]
            #print (intervention_category, metastases_location, exercise_level)
            #print (type(intervention_category), type(metastases_location), type(exercise_level))
            source = media_data.MEDIA_FILE[intervention_category][metastases_location][exercise_level]
    # interventions other than exercise
    else:
        intervention_category = intervention_info_sum[0]
        intervention_progress = int(intervention_info_sum[1])
        source = media_data.MEDIA_FILE[intervention_category][intervention_progress]
    return source


def check_login_same_day(last_login_timestamp):
    current_date = datetime.now()
    last_login_date = datetime.fromtimestamp(last_login_timestamp)

    # assumes all users are in the EST timezone
    EST = pytz.timezone('US/Eastern')
    last_login_date_EST = last_login_date.astimezone(EST)
    current_date_EST = current_date.astimezone(EST)
 
    if ((current_date_EST.day != last_login_date_EST.day) or 
        (current_date_EST.month != last_login_date_EST.month) or
        (current_date_EST.year != last_login_date_EST.year)):
        return False
    #user logs in again on the same day
    else:
        return True

def checkPainAndDistress(session_attr):
    if int(session_attr['pain_value']) >= 7:
        return 'Be sure to contact the clinical care team regarding your pain level.'
    elif int(session_attr['distress_value']) >= 7:
        return 'Be sure to contact the clinical care team regarding your distress level.'
    elif (int(session_attr['pain_value']) >= 7) and (int(session_attr['distress_value']) >= 7):
        return 'Be sure to contact the clinical care team regarding your pain and distress level.'
    else:
        return ''


def retrieve_user_intervention_progress(user_id, activity, update=False):
    media_file = media_data.MEDIA_FILE[activity]
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Nurse_AMIE_User_Progress_Status')
    response = table.query(
        KeyConditionExpression = Key('UserID').eq(user_id) & Key('Activity').eq(activity))
    # there is no intervention progress record in the Database
    # write a new intervention progress entry in the DynamoDB
    if (response['Count'] == 0):
        # if the total number of media in this activity is 1
        # then the next intervention should still be this 
        if len(media_file) == 1:
            user_data = {'Activity': activity,'Status': 0}
        # if there are more than 1 media within this activity
        else: 
            if (update == True):
                user_data = {'Activity': activity,'Status': 1}
            else:
                user_data = {'Activity': activity,'Status': 0}
        write_user_data_to_DynamoDB(table = table,
                                user_id = user_id,
                                user_data = user_data)
        return 0
    else:
        # find entry of this activity
        for DB_row in response['Items']: 
            if activity == DB_row['Activity']:
                intervention_progress = int(DB_row['Status']) #convert decimal.Decimal to integer
        if (update == True):
            if intervention_progress == len(media_file)-1:
                user_data = {'Activity': activity,'Status': 0}
            else:
                user_data = {'Activity': activity,'Status': intervention_progress+1}
            write_user_data_to_DynamoDB(table = table,
                                    user_id = user_id,
                                    user_data = user_data)
        return intervention_progress

def need_to_play_get_to_floor(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Nurse_AMIE_User_Progress_Status')
    response = table.query(
        KeyConditionExpression = Key('UserID').eq(user_id) & Key('Activity').eq('get_to_floor'))
    if (response['Count'] == 0):
        # if patients have lower body metastases, then do not need to play get to floor
        if retrieve_metastases_location(user_id) == 'lower body':
            return False
        else:
            return True
    return False


def retrieve_metastases_location(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Nurse_AMIE_User_Progress_Status')
    response = table.query(
        KeyConditionExpression = Key('UserID').eq(user_id) & Key('Activity').eq('metastases_status'))
    if response['Count'] == 0:
        return None
    else:
        return response['Items'][0]['Status']

def retrieve_exercise_level(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Nurse_AMIE_User_Progress_Status')
    response = table.query(
        KeyConditionExpression = Key('UserID').eq(user_id) & Key('Activity').eq('exercise_level'))
    if response['Count'] == 0:
        user_data = {'Activity': 'exercise_level', 'Status': 1}
        write_user_data_to_DynamoDB(table = table, 
                                user_id = user_id, 
                                user_data = user_data)
        return '1'
    else:
        return str(response['Items'][0]['Status'])



def retrieve_user_nutrition_progress(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Nurse_AMIE_User_Nutrition_Status')
    response = table.query(
        KeyConditionExpression = Key('UserID').eq(user_id))
    if response['Count'] == 0:
        user_data = {'Status': 0}
        write_user_data_to_DynamoDB(table = table, 
                                user_id = user_id, 
                                user_data = user_data, 
                                log_timestamp=True)
        return 0
    else:
        user_latest_login = int(response['Items'][-1]['Datetime'])
        nutrition_progress = response['Items'][-1]['Status']
        if not(check_login_same_day(user_latest_login)):
            user_data = {'Status': nutrition_progress+1}
            nutrition_progress += 1
            write_user_data_to_DynamoDB(table = table, 
                                    user_id = user_id, 
                                    user_data = user_data, 
                                    log_timestamp=True)
        return nutrition_progress





def multi_media_control(response_builder, media_type, source):
    if media_type == 'video':
        play_video = VideoItem(source=source)
        response_builder.add_directive(LaunchDirective(video_item=play_video))
    elif media_type == 'audio':
        audio_stream = Stream(url=source, token = source)
        play_audio = AudioItem(stream=audio_stream)
        response_builder.add_directive(
            PlayDirective(
                play_behavior=PlayBehavior.REPLACE_ALL,
                audio_item=play_audio))
    return response_builder.set_should_end_session(False)
        
def load_URL_content(response_builder, token, source):
    response_builder.add_directive(
    ExecuteCommandsDirective(
        token=token,
        commands=[
            OpenUrlCommand(
            source=source)]))
    return response_builder.set_should_end_session(False)


def get_user_profile(access_token, user_info):
    url = "https://api.amazon.com/user/profile?access_token=" + access_token
    data = requests.get(url).json()
    return data[user_info]

# controller for APL Audio
class AudioController:
    @staticmethod
    def play(response_builder, source, offset_in_ms):
        # type: (HandlerInput) -> Response
        response_builder.add_directive(
            PlayDirective(
                play_behavior=PlayBehavior.REPLACE_ALL,
                audio_item=AudioItem(
                    stream=Stream(
                        token=source,
                        url= source,
                        offset_in_milliseconds=offset_in_ms,
                        expected_previous_token=None),
                    metadata=None)))
        return response_builder
        
    @staticmethod
    def stop(response_builder):
        # type: (HandlerInput) -> Response
        response_builder.add_directive(StopDirective())
        return response_builder

# controller for APL Video
class VideoController:
    @staticmethod
    def play(response_builder, token):
        response_builder.add_directive(
            ExecuteCommandsDirective(
                token=token,
                commands=[
                    ControlMediaCommand(
                    component_id="VideoPlayer",
                    command = 'play')]))
        return response_builder

    @staticmethod
    def stop(response_builder, token):
        response_builder.add_directive(
            ExecuteCommandsDirective(
                token=token,
                commands=[
                    ControlMediaCommand(
                    component_id="VideoPlayer",
                    command = 'pause')]))
        return response_builder

    

    
    
    
    
    
    
    
    
    
