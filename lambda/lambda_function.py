import boto3
import logging
import os
import ask_sdk_core.utils as ask_utils
#from ask_sdk_core.skill_builder import SkillBuilder

from ask_sdk_core.skill_builder import CustomSkillBuilder 
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler

from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.slu.entityresolution import StatusCode
from ask_sdk_model.dialog import (
    ElicitSlotDirective, DelegateDirective)
from ask_sdk_model import (
    Response, IntentRequest, DialogState, SlotConfirmationStatus, Slot, Intent)

from ask_sdk_core.utils import is_intent_name, get_dialog_state, get_slot_value, is_request_type, get_account_linking_access_token

from ask_sdk_core.api_client import DefaultApiClient

from ask_sdk_model.interfaces.alexa.presentation.apl import (
    RenderDocumentDirective, AnimatedOpacityProperty, AnimateItemCommand,
    ExecuteCommandsDirective, UserEvent)


from ask_sdk_model.interfaces.audioplayer import PlayerActivity

from alexa import data, util, nutrition_data, media_data

from ask_sdk_model import Response
from boto3.dynamodb.conditions import Key, Attr
import requests
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        # render welcome page
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr['login_time'] = int(datetime.timestamp(datetime.now()))
        table = dynamodb.Table('Nurse_AMIE_User_Progress_Status')
        # request user to link their amazon account if account linking access token could not be retrieved 
        if get_account_linking_access_token(handler_input) == None:
            speak_output = data.ASK_ACCOUNT_LINKING_VOICE
            response_builder.set_should_end_session(True)

        # collect user amazon account information: name and email and store it as a session attribute
        else:
            access_token = get_account_linking_access_token(handler_input)
            user_name = util.get_user_profile(access_token, user_info = 'name')
            user_email = util.get_user_profile(access_token, user_info = 'email')
            session_attr['user_email'] = user_email
            user_activity_log = {'Activity': 'LaunchRequest', 'Status': 'true'}
            util.log_user_activity_DB(user_email, user_activity_log)
            # retrieve the possible SAME DAY login for this user from 
            # DynamoDB table: Nurse_AMIE_User_Skill_State
            # have data stored in the DynamoDB table: Nurse_AMIE_User_Skill_State
            skill_state = util.retrieve_same_day_skill_state(user_email)
            
            # user starts Nurse AMIE on a NEW day. 
            if (skill_state == None):
                response_builder = util.render_screen(response_builder, 
                            token = data.WELCOME_DOCUMENT_TOKEN,
                            document = data.WELCOME_DOCUMENT)
                session_attr['skill_state'] = "LaunchRequest"
                table = dynamodb.Table('Nurse_AMIE_User_Progress_Status')

                # if NO entry exist in Nurse_AMIE_User_Progress_Status then regard user as first timer user. 
                # ask her a series of questions regarding bone metastases. 
                if util.check_first_time_user(user_email):
                    speak_output = util.get_welcome_first_time_voice(user_name.split()[0])
                    session_attr['skill_state'] = "ask_metastases_question"
                
                # only ask last time's intervention feedback if user's last time's skill state is "intervention_activity_initated"
                # it means that user has ACTUALLY received intervention activity and no feedback has collected regarding this activity 
                elif util.need_to_ask_intervention_feedback(user_email):
                    # greet user and ask if yesterday's intervention is helpful. 
                    session_attr['skill_state'] = "ask_intervention_feedback"
                    speak_output = util.get_welcome_voice()
                
                # start today's activity without asking last time's intervention activity.
                # user started with Nurse AMIE before, only loged their metastasis location 
                # but did not start any intervention activity
                else:
                    session_attr['skill_state'] = "start_nutrition_topic_of_day"
                    speak_output = data.ASK_USER_START_INTERVENTION

            # User has interacted with Nurse AMIE, their skill progress is recorded in the database. 
            # if user has answered the feedback of yesterday's activity
            elif (skill_state == 'yesterday_intervention_feedback_ended'):
                response_builder = util.render_screen(response_builder, 
                            token = data.WELCOME_DOCUMENT_TOKEN,
                            document = data.WELCOME_DOCUMENT)
                session_attr['skill_state'] = "start_nutrition_topic_of_day"
                speak_output = data.ASK_USER_START_INTERVENTION

            # if user has been introduced with the nutrition topic of day
            elif (skill_state == 'topic_of_day_ended'):
                user_nutrition_progress = int(util.retrieve_user_nutrition_progress(session_attr['user_email']))
                response_builder = util.render_screen(response_builder, 
                            token = data.NUTRITION_TOPIC_OF_DAY_NO_SPEAKITEM_TOKEN,
                            document = data.NUTRITION_TOPIC_OF_DAY_NO_SPEAKITEM_DOCUMENT,
                            datasources = util.create_topic_of_day_datasource(user_nutrition_progress))
                session_attr['skill_state'] = "ask_user_symptom_question"
                speak_output = data.ASK_USER_START_SYMPTOM_QUESTIONS
            
            # if user has NOT finished inputing the user_symptom_question. 
            elif (skill_state == 'ask_user_symptom_question'):
                response_builder = util.render_screen(response_builder, 
                            token = data.WELCOME_DOCUMENT_TOKEN,
                            document = data.WELCOME_DOCUMENT)
                session_attr['skill_state'] = "ask_user_symptom_question"
                speak_output = data.ASK_USER_START_SYMPTOM_QUESTIONS
            
            # if today's intervention activity has been introduced to the user. 
            elif (skill_state == 'intervention_activity_initated'):
                response_builder = util.render_screen(response_builder, 
                            token = data.WELCOME_DOCUMENT_TOKEN,
                            document = data.WELCOME_DOCUMENT)
                session_attr['skill_state'] = "review_intervention_activity"
                speak_output = data.ASK_USER_REVIEW_INTERVENTION
            # user has not opened the skill today
            # then direct to Topic of the Day Intro and daily intervention activity 
        return response_builder.speak(speak_output).ask(speak_output).response


class HomeIntentHandler(AbstractRequestHandler):
    """Handler for Home Intent: return to home page 
                                (the same screen content as the Launch Request). 

    Screen Trigger: "apl_back" <- data.PINK_RIBBON_DOCUMENT
    Voice Trigger: "HomeIntent"
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("HomeIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        session_attr = handler_input.attributes_manager.session_attributes
        # directs to Topic of Day Intro Intent
        skill_state = util.retrieve_same_day_skill_state(session_attr['user_email'])

        # if user has NOT finished inputing the symptom_level_question. 
        # ask user to continue with inputing her symptom level history
        if skill_state == 'ask_user_symptom_question':
            session_attr['skill_state'] = "ask_user_symptom_question"
            speak_output = data.ASK_USER_START_SYMPTOM_QUESTIONS

        # if today's intervention activity has been introduced to the user. 
        elif skill_state == 'intervention_activity_initated':
            session_attr['skill_state'] = "review_intervention_activity"
            speak_output = data.ASK_USER_REVIEW_INTERVENTION
        
        # user has not answered the metaastasis question.
        # OR user has finished answering yesterday's intervention activity.
        else:
            # ask user metastases question
            if util.retrieve_metastases_location(session_attr['user_email']) == None:
                session_attr['skill_state'] = "ask_metastases_question"
                speak_output = "Let's continue with my previous question. Do you have bone metastases? You can answer yes or no."
            elif util.need_to_ask_intervention_feedback(session_attr['user_email']):
                # greet user and ask if yesterday's intervention is helpful. 
                session_attr['skill_state'] = "ask_intervention_feedback"
                speak_output = util.get_welcome_voice()
            else:
                session_attr['skill_state'] = "start_nutrition_topic_of_day"
                speak_output = data.ASK_USER_START_INTERVENTION
        response_builder = util.render_screen(response_builder, 
                                            token = data.WELCOME_DOCUMENT_TOKEN,
                                            document = data.WELCOME_DOCUMENT)
        util.log_intent_activity_DB(handler_input, session_attr, "HomeIntent")
        return response_builder.speak(speak_output).ask(speak_output).response




class PinkRibbonIntentHandler(AbstractRequestHandler):
    """Handler for Pink Ribbon Intent: opens menu(pink ribbon)

    Voice Trigger: "PinkRibbonIntent"
    Screen Trigger: "pink_ribbon" <- data.WELCOME_DOCUMENT_TOKEN
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ((is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and 
                list(handler_input.request_envelope.request.arguments)[0] == "pink_ribbon") or
                (is_intent_name("PinkRibbonIntent")(handler_input)))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        speak_output = 'Which activity would like to select?'
        session_attr = handler_input.attributes_manager.session_attributes
        response_builder = util.render_screen(response_builder, 
                                            token = data.PINK_RIBBON_TOKEN,
                                            document = data.PINK_RIBBON_DOCUMENT)
        session_attr['skill_state'] = "PinkRibbonIntent"
        util.log_intent_activity_DB(handler_input, session_attr, "PinkRibbonIntent")
        return response_builder.speak(speak_output).ask(speak_output).response



class RespondYesterdayInterventionFeedbackIntentHandler(AbstractRequestHandler):
    """ respond to user's feedback on yester's intervention activity
        After user said Yes or No

    Backend Trigger: "YesNoIntentHandler"
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("RespondYesterdayInterventionFeedbackIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        session_attr = handler_input.attributes_manager.session_attributes
        # retrieve last time's intervention activity
        intervention_info_sum = util.retrieve_user_intervention_activity(session_attr['user_email'])
        # if the user feedback is positive, then no follow up questions should be asked
        if session_attr['intervention_feedback'] == 'positive':
            session_attr['skill_state'] = "start_nutrition_topic_of_day"
            speak_output = 'I am glad to hear that I helped! Would you like to start today\'s activity?'
            
            # log the feedback to Database: Nurse_AMIE_User_Intervention_Feedback
            util.log_user_intervention_feedback(user_id = session_attr['user_email'], 
                                                intervention_activity = intervention_info_sum,
                                                intervention_feedback = "positive")
            util.log_skill_state_DynamoDB(session_attr['user_email'], 
                                        skill_state = 'yesterday_intervention_feedback_ended')
        # if the user feedback is negative, ask feedback questions if yesterday's activity is exercise
        else:
            # if yesterday's intervention belongs to exercise, ask follow-up questions
            # yesterday's intervention is the newest record in the Nurse_AMIE_User_Symptom_Status 
            intervention_category = intervention_info_sum[0]
            if ((intervention_category == 'balance') or (intervention_category == 'strengthening') or 
                (intervention_category == 'stretching')):
                session_attr['skill_state'] = "AskExerciseLevelIntent"
                speak_output = 'Was your last time\'s exercise too hard, too easy, or it was just right?'
                response_builder = util.elicit_slot(response_builder, 
                                                    slot_to_elicit = "exercise_level", 
                                                    next_intent = "AskExerciseLevelIntent")
            # no need to ask follow up questions
            else:
                # log the feedback to Database: Nurse_AMIE_User_Intervention_Feedback
                util.log_user_intervention_feedback(user_id = session_attr['user_email'], 
                                                    intervention_activity = intervention_info_sum,
                                                    intervention_feedback = "negative")
                session_attr['skill_state'] = "start_nutrition_topic_of_day"
                speak_output = 'Sorry to hear that! I will work harder! Would you like to start today\'s activity?'
                util.log_skill_state_DynamoDB(session_attr['user_email'], 
                                            skill_state = 'yesterday_intervention_feedback_ended')
        util.log_intent_activity_DB(handler_input, session_attr, "RespondInterventionFeedbackIntent")
        return response_builder.speak(speak_output).ask(speak_output).response



class AskMetastasesLocationIntentHandler(AbstractRequestHandler):
    """Ask Metastasis Location if user said YES whether they have bone Metastasis

    Elicit Trigger: "YesNoIntent"
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AskMetastasesLocationIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        session_attr = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots
        # user's response matches with the predefined answer
        # store the location of metastases
        if (util.er_success_match(slots['location'])):
            # users need to confirm the location of metastases before starting new intervention activity 
            session_attr['skill_state'] = "confirm_metastases_question"
            # get the metastases location from the slot in AskMetastasesLocationIntent
            metastases_location = util.log_slot_resolutions_value(slots['location'])
            session_attr['metastases_location'] = metastases_location
            # generate speak output to confirm the location of metastases location
            if metastases_location == "torso":
                speak_output = "Thank you! Just to confirm, your bone metastases is located at torso or spine. Am I right?"
            else:
                speak_output = ("Thank you! Just to confirm, your bone metastases is located at " + metastases_location + 
                                ". Am I right?")
        # user's response DOES NOT match with the predefined answer        
        else:
            response_builder = util.elicit_slot(response_builder, 
                                                slot_to_elicit = "location")
            speak_output = 'You can say torso or spine, or upper body, or lower body.'
        #session_attr['skill_state'] = "NutritionHomepageIntent"
        util.log_intent_activity_DB(handler_input, session_attr, "AskMetastasesLocationIntent")
        return response_builder.speak(speak_output).ask(speak_output).response



class AskExerciseLevelIntentHandler(AbstractRequestHandler):
    """ Ask the follow-up question of intervention feedback, 
        Ask if the exercise intervention is too hard/ too easy/ just right

    Elicit Trigger: "RespondYesterdayInterventionFeedbackIntent"
                    "AskExerciseLevelIntent"; 
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AskExerciseLevelIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        session_attr = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots

        # user's response matches with the predefined answer
        if (util.er_success_match(slots['exercise_level'])):
            session_attr['skill_state'] = "start_nutrition_topic_of_day"
            speak_output = 'ok, I get your answer! Would you like to start today\'s activity?'            
            # log users' feedback on last time's intervention activity 
            intervention_info_sum = util.retrieve_user_intervention_activity(session_attr['user_email'])
            util.log_user_intervention_feedback(user_id = session_attr['user_email'], 
                                        intervention_activity = intervention_info_sum,
                                        intervention_feedback = "negative", 
                                        exercise_level_feedback = util.log_slot_resolutions_value(slots['exercise_level']))

            # update user's exercise level in Nurse_AMIE_User_Progress_Status
            # also generate the speak out according to the update
            speak_output = util.update_user_exercise_level(user_id = session_attr['user_email'],
                                            exercise_level_feedback = util.log_slot_resolutions_value(slots['exercise_level']))
            speak_output += 'Would you like to start today\'s activity?'
        # user's response DOES NOT match with the predefined answer        
        else:
            response_builder = util.elicit_slot(response_builder, 
                                                slot_to_elicit = "exercise_level")
            speak_output = 'You can say too hard, too easy, or just right.'
        #session_attr['skill_state'] = "NutritionHomepageIntent"
        util.log_intent_activity_DB(handler_input, session_attr, "AskExerciseLevelIntent")
        return response_builder.speak(speak_output).ask(speak_output).response



class NutritionHomepageIntentHandler(AbstractRequestHandler):
    """opens the main menu for Nutrition

    Voice Trigger: "NutritionHomepageIntent"
    Screen Trigger: "nutrition_homepage" <- data.PINK_RIBBON_DOCUMENT
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ((is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and 
                list(handler_input.request_envelope.request.arguments)[0] == "nutrition_homepage") or
                (is_intent_name("NutritionHomepageIntent")(handler_input)))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        session_attr = handler_input.attributes_manager.session_attributes
        speak_output = 'What are you looking for? New recipe, recipe category or favourite recipe?'
        response_builder = util.render_screen(response_builder, 
                                            token = data.NUTRITION_HOMEPAGE_TOKEN,
                                            document = data.NUTRITION_HOMEPAGE_DOCUMENT)
        session_attr['skill_state'] = "NutritionHomepageIntent"
        util.log_intent_activity_DB(handler_input, session_attr, "NutritionHomepageIntent")
        return response_builder.speak(speak_output).ask(speak_output).response



class LoadFavouriteRecipeListIntentHandler(AbstractRequestHandler):
    """loads the list of favourite recipes

    Voice Trigger: "LoadFavouriteRecipeListIntent"
    Screen Trigger: "open_recipe_list_favourite" <- data.NUTRITION_HOMEPAGE_DOCUMENT
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ((is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and 
                list(handler_input.request_envelope.request.arguments)[0] == "open_recipe_list_favourite") or
                (is_intent_name("LoadFavouriteRecipeListIntent")(handler_input)))

    def handle(self, handler_input): 
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        session_attr = handler_input.attributes_manager.session_attributes
        speak_output = 'Here are your favourite recipes. Please use the touch screen to select.'
        apl_datasources = util.create_bookmarked_list_datasource(session_attr['user_email'])
        response_builder = util.render_screen(response_builder, 
                                            token = data.NUTRITION_FAVOURITE_LIST_TOKEN,
                                            document = data.NUTRITION_FAVOURITE_LIST_DOCUMENT,
                                            datasources = apl_datasources)
        session_attr['skill_state'] = "LoadFavouriteRecipeListIntent"
        util.log_intent_activity_DB(handler_input, session_attr, "LoadFavouriteRecipeListIntent")
        return response_builder.speak(speak_output).response


class LoadRecipeCategoryIntentHandler(AbstractRequestHandler):
    """loads the list of recipes' category; 
        it will only show the categories that a user has seen before. 

    Voice Trigger: "LoadRecipeCategoryIntent"
    Screen Trigger: "open_recipe_list_category" <- data.NUTRITION_HOMEPAGE_DOCUMENT
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ((is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and 
                list(handler_input.request_envelope.request.arguments)[0] == "open_recipe_list_category") or
                (is_intent_name("LoadRecipeCategoryIntent")(handler_input)))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        #retrieve user's nutrition progress from DynamoDB
        session_attr = handler_input.attributes_manager.session_attributes
        user_nutrition_progress = int(util.retrieve_user_nutrition_progress(session_attr['user_email']))
        session_attr['nutrition_progress'] = user_nutrition_progress
        apl_datasources = util.create_recipe_category_datasource(user_nutrition_progress)
        response_builder = util.render_screen(response_builder, 
                                            token = data.RECIPE_CATEGORY_TOKEN,
                                            document = data.RECIPE_CATEGORY_DOCUMENT,
                                            datasources = apl_datasources)
        speak_output = 'Here are the recipes\' category. Please use the touch screen to select.'
        session_attr['skill_state'] = "LoadRecipeCategoryIntent"
        util.log_intent_activity_DB(handler_input, session_attr, "LoadRecipeCategoryIntent")
        return response_builder.speak(speak_output).response


class LoadRecipeListByCategoryIntentHandler(AbstractRequestHandler):
    """loads the list of recipes within a category; 
            it will only show the recipes that a user has seen before. 

        Voice Trigger: N/A
        Screen Trigger: "open_target_category， "${LambdaData.properties.title}"" <- data.RECIPE_CATEGORY_DOCUMENT
                        "apl_back" <- data.NUTRITION_CATEGORY_RECIPE_INTRO_DOCUMENT
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and 
                list(handler_input.request_envelope.request.arguments)[0] == "open_target_category")

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        session_attr = handler_input.attributes_manager.session_attributes
        if 'recipe_category_title' not in session_attr:
            session_attr['recipe_category_title'] = list(handler_input.request_envelope.request.arguments)[1]
        category_title = session_attr['recipe_category_title']
        apl_datasources = util.create_target_category_list_datasource(category_title, session_attr['nutrition_progress'])
        response_builder = util.render_screen(response_builder, 
                                                token = data.RECIPE_CATEGORY_LIST_TOKEN,
                                                document = data.RECIPE_CATEGORY_LIST_DOCUMENT,
                                                datasources = apl_datasources)
        speak_output = 'Here are the recipes for {}. Please use the touch screen to select.'.format(category_title)
        session_attr['category_title'] = category_title
        session_attr['skill_state'] = "LoadRecipeListByCategoryIntent"
        util.log_intent_activity_DB(handler_input, session_attr, "LoadRecipeListByCategoryIntent")
        return response_builder.speak(speak_output).response


class BookmarkRecipeIntentHandler(AbstractRequestHandler):
    """loads the list of recipes within a category; 
            it will only show the recipes that a user has seen before. 

    Voice Trigger: "BookmarkRecipeIntent"
    Screen Trigger: "bookmark_recipe" <- data.NUTRITION_NEW_RECIPE_INTRO_TOKEN;
                                         data.NUTRITION_CATEGORY_RECIPE_INTRO_TOKEN;
                                         data.NUTRITION_FAVOURITE_RECIPE_INTRO_TOKEN
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ((is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and 
                list(handler_input.request_envelope.request.arguments)[0] == "bookmark_recipe") or
                (is_intent_name("BookmarkRecipeIntent")(handler_input)))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        session_attr = handler_input.attributes_manager.session_attributes
        speak_output = 'All set! This recipe is saved!'
        # log recipe data to DynamoDB: Nurse_AMIE_User_Nutrition_Bookmark
        util.addRecipeToBookmark(session_attr['user_email'], session_attr['recipe_title'], session_attr['recipe_id'])
        util.log_intent_activity_DB(handler_input, session_attr, "BookmarkRecipeIntent")
        return response_builder.speak(speak_output).response



class LoadRecipeIntroIntentHandler(AbstractRequestHandler):
    """loads the introduction page of a recipe; it could be triggered from 3 sources.  

    Voice Trigger: "OpenNewRecipeIntent"
    Screen Trigger: "open_recipe_intro" <- data.NUTRITION_HOMEPAGE_DOCUMENT;
                    "open_recipe_intro, "${recipe_id}", " <- data.RECIPE_CATEGORY_LIST_DOCUMENT;
                    "open_recipe_intro, "${recipe_id}" <- data.NUTRITION_FAVOURITE_LIST_DOCUMENT
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ((is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and
                (list(handler_input.request_envelope.request.arguments)[0] == "open_recipe_intro")) or
                (is_intent_name("OpenNewRecipeIntent")(handler_input)))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        session_attr = handler_input.attributes_manager.session_attributes

        # if the recipe intro is accessed from nutrition homepage
        # load a new daily recipe
        if session_attr['skill_state'] == 'NutritionHomepageIntent':
            user_nutrition_progress = int(util.retrieve_user_nutrition_progress(session_attr['user_email']))
            recipe_data = nutrition_data.RECIPE_SCHEDULE[user_nutrition_progress]
            session_attr['skill_state'] = "LoadRecipeIntroIntent_NewRecipe"
            speak_output = 'Today, I introduce you to {}! Hope you enjoy!!'.format(recipe_data['title'])

        # if the recipe intro is accessed from recipe list of a category. 
        # find the recipe details according to the recipe id
        elif session_attr['skill_state'] == 'LoadRecipeListByCategoryIntent':
            speak_output = 'Here is the recipe.'
            recipe_id = list(handler_input.request_envelope.request.arguments)[1]
            recipe_data = util.find_recipe(recipe_id=recipe_id)
            session_attr['skill_state'] = "LoadRecipeIntroIntent_RecipeCategory"

        # if the recipe intro is accessed from the favourite recipe list. 
        # find the recipe details according to the recipe id
        else:
            speak_output = 'Here is the recipe.'
            recipe_id = list(handler_input.request_envelope.request.arguments)[1]
            recipe_data = util.find_recipe(recipe_id=recipe_id)
            session_attr['skill_state'] = "LoadRecipeIntroIntent_FavRecipe"
            
        # used in LaunchRecipeURLIntentHandler
        session_attr['recipe_url'] = recipe_data['link']
        # used in BookmarkRecipeIntent
        session_attr['recipe_title'] = recipe_data['title']
        session_attr['recipe_id'] = recipe_data['id']
        # load the recipe intro page
        response_builder = util.render_screen(response_builder, 
                                                token = data.NUTRITION_CATEGORY_RECIPE_INTRO_TOKEN,
                                                document = data.NUTRITION_RECIPE_INTO_DOCUMENT,
                                                datasources = util.create_recipe_summary_datasource(recipe_data))
        util.log_intent_activity_DB(handler_input, session_attr, "OpenRecipeIntroIntent")
        return response_builder.speak(speak_output).response


class LaunchRecipeURLIntentHandler(AbstractRequestHandler):
    """loads the Recipe URL in Amazon Silk browser; 

    Voice Trigger: "LaunchRecipeURLIntent"
    Screen Trigger: "open_recipe_detail" <- data.NUTRITION_RECIPE_INTO_DOCUMENT;
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ((is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and 
                list(handler_input.request_envelope.request.arguments)[0] == "open_recipe_detail") or
                (is_intent_name("LaunchRecipeURLIntent")(handler_input)))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        speak_output = 'OK! I will direct you to the recipe detail. '
        session_attr = handler_input.attributes_manager.session_attributes
        token = handler_input.request_envelope.context.alexa_presentation_apl.token
        response_builder = util.load_URL_content(response_builder, 
                                                    token = token, 
                                                    source = session_attr['recipe_url'])
        session_attr['skill_state'] = "LaunchRecipeURLIntent"
        util.log_intent_activity_DB(handler_input, session_attr, "LaunchRecipeURLIntent")
        return response_builder.speak(speak_output).response


class MovementsIntentHandler(AbstractRequestHandler):
    """loads the Movement Menu; 

    Voice Trigger: "MovementsIntent"
    Screen Trigger: "movements" <- data.PINK_RIBBON_DOCUMENT;
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ((is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and 
                list(handler_input.request_envelope.request.arguments)[0] == "movements") or
                (is_intent_name("MovementsIntent")(handler_input)))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        session_attr = handler_input.attributes_manager.session_attributes
        speak_output = 'Please browse through the contents and use the touch screen to select the activity.'
        metastases_location = util.retrieve_metastases_location(session_attr['user_email'])
        if metastases_location == None:
            speak_output = "Sorry, you do not have the access yet. I need to know your bone metastases information first. Thank you."
            return response_builder.speak(speak_output).response
        if metastases_location == 'no met':
            apl_document = data.MOVEMENT_LIST_NO_MET_DOCUMENT
        elif metastases_location == 'upper body':
            apl_document = data.MOVEMENT_LIST_UPPER_BODY_DOCUMENT
        elif metastases_location == 'lower body':
            apl_document = data.MOVEMENT_LIST_LOWER_BODY_DOCUMENT
        else:
            apl_document = data.MOVEMENT_LIST_TORSO_DOCUMENT
        response_builder = util.render_screen(response_builder, 
                                                token = data.MOVEMENT_LIST_TOKEN,
                                                document = apl_document)
        session_attr['skill_state'] = "MovementsIntent"
        util.log_intent_activity_DB(handler_input, session_attr, "MovementsIntent")
        return response_builder.speak(speak_output).response


class CopingSymptomsIntentHandler(AbstractRequestHandler):
    """loads the Coping Symptoms Menu; 

    Voice Trigger: "CopingSymptomsIntent"
    Screen Trigger: "coping_symptoms" <- data.PINK_RIBBON_DOCUMENT;
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ((is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and 
                list(handler_input.request_envelope.request.arguments)[0] == "coping_symptoms") or
                (is_intent_name("CopingSymptomsIntent")(handler_input)))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        session_attr = handler_input.attributes_manager.session_attributes
        speak_output = 'Please browse through the contents and use the touch screen to select the activity.'
        response_builder = util.render_screen(response_builder, 
                                                token = data.COPING_SYMPTOMS_LIST_TOKEN,
                                                document = data.COPING_SYMPTOMS_LIST_DOCUMENT)
        session_attr['skill_state'] = "CopingSymptomsIntent"
        util.log_intent_activity_DB(handler_input, session_attr, "CopingSymptomsIntent")
        return response_builder.speak(speak_output).response


class SoothingMusicIntentHandler(AbstractRequestHandler):
    """loads the Soothing Music Menu; 

    Voice Trigger: "SoothingMusicIntent"
    Screen Trigger: "soothing_music" <- data.PINK_RIBBON_DOCUMENT;
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ((is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and 
                list(handler_input.request_envelope.request.arguments)[0] == "soothing_music") or
                (is_intent_name("SoothingMusicIntent")(handler_input)))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        session_attr = handler_input.attributes_manager.session_attributes
        speak_output = 'Please browse through the contents and use the touch screen to select the activity.'
        response_builder = util.render_screen(response_builder, 
                                                token = data.SOOTHING_MUSIC_LIST_TOKEN,
                                                document = data.SOOTHING_MUSIC_LIST_DOCUMENT)
        session_attr['skill_state'] = "SoothingMusicIntent"
        util.log_intent_activity_DB(handler_input, session_attr, "SoothingMusicIntent")
        return response_builder.speak(speak_output).response


class GuidedRelaxationIntentHandler(AbstractRequestHandler):
    """loads the Guided Relaxation Menu; 

    Voice Trigger: "GuidedRelaxationIntent"
    Screen Trigger: "guided_relaxation" <- data.PINK_RIBBON_DOCUMENT;
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ((is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and 
                list(handler_input.request_envelope.request.arguments)[0] == "guided_relaxation") or
                (is_intent_name("GuidedRelaxationIntent")(handler_input)))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        session_attr = handler_input.attributes_manager.session_attributes
        speak_output = 'Please browse through the contents and use the touch screen to select the activity.'
        response_builder = util.render_screen(response_builder, 
                                                token = data.GUIDED_RELAXATION_LIST_TOKEN,
                                                document = data.GUIDED_RELAXATION_LIST_DOCUMENT)
        session_attr['skill_state'] = "GuidedRelaxationIntent"
        util.log_intent_activity_DB(handler_input, session_attr, "GuidedRelaxationIntent")
        return response_builder.speak(speak_output).response


class PlayUserSelectedActivityIntentHandler(AbstractRequestHandler):
    """plays the user selected media from PINK RIBBON

    Voice Trigger: NA
    Screen Trigger: ["selected_activity","movements", "3"] <- data.MOVEMENT_LIST_DOCUMENT;
                                                           <- data.COPING_SYMPTOMS_LIST_DOCUMENT;
                                                           <- data.SOOTHING_MUSIC_LIST_DOCUMENT;
                                                           <- data.GUIDED_RELAXATION_LIST_DOCUMENT
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and 
                list(handler_input.request_envelope.request.arguments)[0] == "selected_activity")

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        session_attr = handler_input.attributes_manager.session_attributes
        intervention_category = list(handler_input.request_envelope.request.arguments)[1]

        if ((intervention_category == 'balance') or (intervention_category == 'stretching') or 
            (intervention_category == 'strengthening')):
            metastases_location = util.retrieve_metastases_location(session_attr['user_email'])
            intervention_index = list(handler_input.request_envelope.request.arguments)[2]
            source = media_data.MEDIA_FILE[intervention_category][metastases_location][intervention_index]
        else:
            intervention_index = int(list(handler_input.request_envelope.request.arguments)[2])
            source = media_data.MEDIA_FILE[intervention_category][intervention_index]
        response_builder = util.multi_media_control(response_builder,
                                        media_type = media_data.MEDIA_TYPE[intervention_category],
                                        source = source)
        user_activity_log = {'Activity': 'PlayUserSelectedActivityIntent', 'Status': intervention_category + ' ' +str(intervention_index)}
        util.log_user_activity_DB(session_attr['user_email'], user_activity_log)
        return (response_builder.response)


class TopicOfDayIntroIntentHandler(AbstractRequestHandler):
    """ Introduce Nutrition Topic of Day Introduction 

    Voice Trigger: NA
    Screen Trigger: NA
    Backend Trigger: YesNoIntent <- if user answers yes in LaunchRequest.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("TopicOfDayInfoIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        slots = handler_input.request_envelope.request.intent.slots
        session_attr = handler_input.attributes_manager.session_attributes
        util.log_intent_activity_DB(handler_input, session_attr, "TopicOfDayIntroIntent")
        # user select to start Topic of Day Intro
        user_nutrition_progress = int(util.retrieve_user_nutrition_progress(session_attr['user_email']))
        session_attr['nutrition_progress'] = user_nutrition_progress
        response_builder = util.render_screen(response_builder, 
                                            token = data.NUTRITION_TOPIC_OF_DAY_TOKEN,
                                            document = data.NUTRITION_TOPIC_OF_DAY_DOCUMENT,
                                            datasources = util.create_topic_of_day_datasource(user_nutrition_progress))
        util.log_skill_state_DynamoDB(session_attr['user_email'], 
                                            skill_state = 'topic_of_day_ended')
        session_attr['skill_state'] = "TopicOfDayIntroIntent"
        speak_output = util.create_topic_of_day_speak(user_nutrition_progress)
        return response_builder.speak(speak_output).response



class TopicOfDayMoreInfoIntentHandler(AbstractRequestHandler):
    """loads the Topic of Day URL in Amazon Silk browser; 

    Voice Trigger: "TopicOfDayMoreInfoIntent"
    Screen Trigger: ["topic_of_day_more_info"] <- data.NUTRITION_TOPIC_OF_DAY_DOCUMENT;
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ((is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and 
                list(handler_input.request_envelope.request.arguments)[0] == "topic_of_day_more_info") or
                (is_intent_name("TopicOfDayMoreInfoIntent")(handler_input)))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        session_attr = handler_input.attributes_manager.session_attributes
        speak_output = ("I will direct you to a web browser. If you would like to "
                        "proceed with the intervention activities, please come back to Nurse AMIE!")
        URL_source = nutrition_data.TOPIC_OF_DAY_SCHEDULE[session_attr['nutrition_progress']]['link']
        response_builder = util.load_URL_content(response_builder, 
                                                    token = data.NUTRITION_TOPIC_OF_DAY_TOKEN, 
                                                    source = URL_source)
        session_attr['skill_state'] = "TopicOfDayMoreInfoIntent"
        util.log_intent_activity_DB(handler_input, session_attr, "TopicOfDayMoreInfoIntent")
        return response_builder.speak(speak_output).response



class AskSymptomLevelIntentHandler(AbstractRequestHandler):
    """Ask a series symptom level questions to user; 

    Voice Trigger: "AskSymptomLevelIntent"
    Screen Trigger: NA;
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AskSymptomLevelIntent")(handler_input))
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Responses
        session_attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        slots = handler_input.request_envelope.request.intent.slots
        datasources = {'LambdaData':{None: None}}
        util.log_skill_state_DynamoDB(session_attr['user_email'], 
                                    skill_state = 'ask_user_symptom_question')
        session_attr['skill_state'] = "AskSymptomLevelIntent"
        # user select to continue with Nurse AMIE
        # iterate through each of the symptom level questions
        for slot_var in data.GUIDED_SLOT:
            if util.not_match_guided_slot_match(slots,slot_var,session_attr):
                session_attr[slot_var] = None
                speak_output = util.ask_guided_activity_slot(slot_var, data.SLOT_ASK_VOICE)
                response_builder = util.render_screen(response_builder, 
                                                token = data.REQUEST_SYMPTOM_LEVEL_TOKEN,
                                                document = data.REQUEST_SYMPTOM_LEVEL_DOCUMENT,
                                                datasources = data.SYMPTOM_LEVEL_APL_DATASOURCES[slot_var])
                response_builder =  util.elicit_slot(response_builder, 
                                                slot_to_elicit = slot_var)
                user_activity_log = {'Activity': slot_var + 'Intent', 'Status': 'true'}
                util.log_user_activity_DB(session_attr['user_email'], user_activity_log)
                return (response_builder
                    .speak(speak_output).ask(speak_output)
                    .response)
            else:
                if slot_var != 'steps':
                    session_attr[slot_var] = util.log_slot_resolutions_value(slots[slot_var])
                session_attr[slot_var + '_value'] = slots[slot_var].value
                datasources['LambdaData'][slot_var] = slots[slot_var].value
                #if (slot_var == 'pain') or (slot_var == 'distress'
        speak_output = data.CONFIRM_GUIDED_SLOT_VOICE
        response_builder = util.render_screen(response_builder, 
                                            token = data.CONFIRM_GUIDED_SLOT_TOKEN,
                                            document = data.CONFIRM_GUIDED_SLOT_DOCUMENT,
                                            datasources = datasources)
        #user select not to continue
        return (response_builder
            .speak(speak_output).ask(speak_output)
            .response)


class ConfirmSymptomLevelIntentHandler(AbstractRequestHandler):
    """This intent handles the action after user has confirmed the symptom level by saying yes. 
       then ask if user would like to start today's intervention activity. 

    Voice Trigger: NA
    Screen Trigger: NA;
    Backend Trigger: YesNoIntent <- if user answers yes: user confirm symptom level
    """
    def can_handle(self, handler_input):
        return (is_intent_name("ConfirmSymptomLevelIntent")(handler_input))
        
    def handle(self, handler_input):
        response_builder = handler_input.response_builder
        session_attr = handler_input.attributes_manager.session_attributes
        
        # get the intervention category and a speak_output
        # e.g. 'strengthing', 'Let\'s get that body moving. Are you ready?' 
        session_attr['intervention_category'], intervention_intro = util.generateInterventionContent(session_attr)
        
        # check if either or both of PAIN and DISTRESS are higher than 7
        # if so add a reminder in the speak_output
        speak_output = util.checkPainAndDistress(session_attr) + '<break time="1s"/>'  + intervention_intro

        # if intervention belongs to exercise
        if (((session_attr['intervention_category'] == 'balance') or 
            (session_attr['intervention_category'] == 'stretching') or 
            (session_attr['intervention_category'] == 'strengthening'))):
            # retrieve user health status and exercise level from 
            session_attr['met_location'] = util.retrieve_metastases_location(session_attr['user_email'])
            session_attr['exercise_level'] = util.retrieve_exercise_level(session_attr['user_email'])
            # user needs to play get to floor
            if (util.need_to_play_get_to_floor(session_attr['user_email']) == True):
                speak_output = speak_output + '<break time="1s"/>' + data.ASK_USER_GET_TO_FLOOR_FIRST
                response_builder = util.render_screen(response_builder, 
                                                token = data.REQUEST_PLAY_GET_TO_FLOOR_TOKEN,
                                                document = data.REQUEST_PLAY_GET_TO_FLOOR_DOCUMENT)
            # 
            else:
                speak_output = speak_output + '<break time="1s"/>' + data.ASK_USER_START_VIDEO_INTERVENTION_MEDIA
                response_builder = util.render_screen(response_builder, 
                                                token = data.REQUEST_PLAY_VIDEO_INTERVENTION_TOKEN,
                                                document = data.REQUEST_PLAY_VIDEO_INTERVENTION_DOCUMENT)
        # intervention does NOT belongs exercise 
        else:
            # get the intervention progress for this category from DynamoDB and update the progress. 
            session_attr['intervention_progress'] = util.retrieve_user_intervention_progress(user_id = session_attr['user_email'], 
                                                                            activity = session_attr['intervention_category'],
                                                                            update=True)
            media_type = media_data.MEDIA_TYPE[session_attr['intervention_category']]
            # the intervention is video
            if media_type == 'video':
                speak_output = speak_output + '<break time="1s"/>' + data.ASK_USER_START_VIDEO_INTERVENTION_MEDIA
                response_builder = util.render_screen(response_builder, 
                                                    token = data.REQUEST_PLAY_VIDEO_INTERVENTION_TOKEN,
                                                    document = data.REQUEST_PLAY_VIDEO_INTERVENTION_DOCUMENT)
            elif media_type == 'audio':
                speak_output = speak_output + '<break time="1s"/>' + data.ASK_USER_START_AUDIO_INTERVENTION_MEDIA
                response_builder = util.render_screen(response_builder, 
                                                    token = data.REQUEST_PLAY_AUDIO_INTERVENTION_TOKEN,
                                                    document = data.REQUEST_PLAY_AUDIO_INTERVENTION_DOCUMENT)
        
        # this is where to send user data to the API!! comment out for now. 
        # util.send_data_external_api(session_attr)
        
        # log user symptom level to DynamoDB
        util.log_user_symptom_level(session_attr)
        
        # log skill state to DynamoDB 
        util.log_skill_state_DynamoDB(session_attr['user_email'], 
                                    skill_state = 'intervention_activity_initated')
        session_attr['skill_state'] = "ConfirmSymptomLevelIntent"
        # log user activity to DynamoDB
        user_activity_log = {'Activity':  'ConfirmSymptomLevelIntent',
                            'Status': session_attr['intervention_category']}
        util.log_user_activity_DB(session_attr['user_email'], user_activity_log)

        return (response_builder.speak(speak_output).ask(speak_output)
            .response)



class LoadInterventionMediaIntentHandler(AbstractRequestHandler):
    """Play the media file of the daily intervention activity; 

    Voice Trigger: LoadInterventionMediaIntent
    Screen Trigger: ["start_intervention"] <- data.CONFIRM_INTERVENTION_DOCUMENT
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("LoadInterventionMediaIntent")(handler_input) or 
                (is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and 
                list(handler_input.request_envelope.request.arguments)[0] == "start_intervention"))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        session_attr = handler_input.attributes_manager.session_attributes
        # extrct the intervention data from the DynamoDB: Nurse_AMIE_User_Symptom_Status
        # the lengh of intervention_sum is either 2 or 3.
        # exercise: [intervention_category, met_location, exercise_level]
        intervention_info_sum = util.retrieve_user_intervention_activity(session_attr['user_email'])
        intervention_category = intervention_info_sum[0]
        if (intervention_category == 'walking'):
            response_builder.set_should_end_session(True)
        else:
            response_builder = util.multi_media_control(response_builder,
                                                        media_type = media_data.MEDIA_TYPE[intervention_category],
                                                        source = util.get_intervention_url(intervention_info_sum))
            print ('source is')
            print (util.get_intervention_url(intervention_info_sum))
            user_activity_log = {'Activity':  'LoadInterventionMediaIntent', 'Status': 'true'}
            util.log_user_activity_DB(session_attr['user_email'], user_activity_log)
        return (response_builder
            .response)


class PlayGetToFloorVideoIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("PlayGetToFloorVideoIntent")(handler_input) or 
                (is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and 
                list(handler_input.request_envelope.request.arguments)[0] == "play_get_to_floor"))
    
    def handle(self, handler_input):
        response_builder = handler_input.response_builder
        dynamodb = boto3.resource('dynamodb')
        session_attr = handler_input.attributes_manager.session_attributes
        util.multi_media_control(response_builder, 
                                media_type = 'video', 
                                source = 'https://nurse-amie.s3.us-east-2.amazonaws.com/introduction/Getting+to+the+Floor_FINAL_04-13-17.mp4')
        user_data = {'Activity': 'get_to_floor','Status': 'true'}
        util.write_user_data_to_DynamoDB(table = dynamodb.Table('Nurse_AMIE_User_Progress_Status'),
                                    user_id = session_attr['user_email'],
                                    user_data = user_data)
        util.log_intent_activity_DB(handler_input, session_attr, "PlayaGetToFloorVideoIntent")
        return (response_builder.response)



class ChangeGuidedActivityIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ChangeGuidedActivityIntent")(handler_input)
        
    def handle(self, handler_input):
        response_builder = handler_input.response_builder
        slots = handler_input.request_envelope.request.intent.slots
        slot_to_change = slots['symptoms'].value.split()
        session_attr = handler_input.attributes_manager.session_attributes
        datasources = {'LambdaData':{None: None}}
        for slot_var in data.GUIDED_SLOT:
            datasources['LambdaData'][slot_var] = session_attr[slot_var + '_value']
        if all(slot in data.GUIDED_SLOT for slot in slot_to_change):
            for slot_var in slot_to_change:
                if util.match_guided_slot_match(slots,slot_var,session_attr):
                    speak_output = util.ask_guided_activity_slot(slot_var, data.CHANGE_SLOT_ASK_VOICE)
                    slot_to_elicit = slot_var
                    token = data.WELCOME_DOCUMENT_TOKEN
                    document = util.load_apl_document(data.GUIDED_SLOT_DOCUMENT)
                    datasources = data.GUIDED_SLOT_DATASOURCES[slot_var]
                    response_builder = util.elicit_slot(response_builder, slot_to_elicit)
                    response_builder = util.render_document(response_builder, token, document, datasources)
                    user_activity_log = {'Activity': 'Change'+slot_var + 'Intent', 'Status': 'true'}
                    util.log_user_activity_DB(session_attr['user_email'], user_activity_log)
                    return (response_builder
                        .speak(speak_output)
                        .response)
                else:
                    session_attr[slot_var] = util.log_slot_resolutions_value(slots[slot_var])
                    session_attr[slot_var + '_value'] = slots[slot_var].value
                    datasources['LambdaData'][slot_var] = slots[slot_var].value
            slot_to_elicit = "yes_no"
            next_intent = "ConfirmGuidedActivityIntent"
            speak_output = data.CONFIRM_GUIDED_SLOT_VOICE
            document = util.load_apl_document(data.CONFIRM_GUIDED_SLOT_DOCUMENT)
            token = data.CONFIRM_GUIDED_SLOT_TOKEN
            response_builder = util.elicit_slot(response_builder, slot_to_elicit, next_intent)
            response_builder = util.render_document(response_builder, token, document, datasources)
            return (response_builder
                .speak(speak_output)
                .response)
        else:
            speak_output = data.REPROMPT_CHANGE_GUIDED_SLOT_VOICE
            return (response_builder
                .aks(speak_output)
                .response)



class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )



class PauseIntentHandler(AbstractRequestHandler):
    """Handler for pause intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.PauseIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        session_attr = handler_input.attributes_manager.session_attributes
        #pause video player (used in APL Video)
        '''
        if handler_input.request_envelope.context.alexa_presentation_apl is not None:
            user_activity_log = {'Activity': 'PauseVideoVoice', 'Status': 'true'}
            util.log_user_activity_DB(session_attr['user_email'], user_activity_log)
            token = handler_input.request_envelope.context.alexa_presentation_apl.token
            response_builder = util.VideoController.stop(response_builder, token)
        '''
        #pause audio player
        if handler_input.request_envelope.context.audio_player is not None:
            offset_in_ms = handler_input.request_envelope.context.audio_player.offset_in_milliseconds
            access_token = get_account_linking_access_token(handler_input)
            user_email = util.get_user_profile(access_token, user_info = 'email')
            user_activity_log = {'Activity': 'PauseAudio', 'Status': 'voice'}
            util.log_user_activity_DB(user_email, user_activity_log)
            #user_activity_log = {'Activity': 'PauseAudio', 'Status': 'true'}
            #util.log_user_activity_DB(session_attr['user_email'], user_activity_log)
            response_builder = util.AudioController.stop(response_builder)
        #pause video player
        return (response_builder.response)



class ResumeIntentHandler(AbstractRequestHandler):
    """Handler for resume intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.ResumeIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        session_attr = handler_input.attributes_manager.session_attributes
        ####from ask_sdk_model.interfaces.audioplayer import PlayerActivity
        '''
        if handler_input.request_envelope.context.alexa_presentation_apl is not None:
            user_activity_log = {'Activity': 'ResumeVideoVoice', 'Status': 'true'}
            util.log_user_activity_DB(session_attr['user_email'], user_activity_log)
            token = handler_input.request_envelope.context.alexa_presentation_apl.token
            response_builder = util.VideoController.play(response_builder, token)
        '''
        if handler_input.request_envelope.context.audio_player is not None:
            if handler_input.request_envelope.context.audio_player.player_activity == PlayerActivity.STOPPED:
                access_token = get_account_linking_access_token(handler_input)
                user_email = util.get_user_profile(access_token, user_info = 'email')
                user_activity_log = {'Activity': 'ResumeAudio', 'Status': 'voice'}
                util.log_user_activity_DB(user_email, user_activity_log)
                source = handler_input.request_envelope.context.audio_player.token
                offset_in_ms = handler_input.request_envelope.context.audio_player.offset_in_milliseconds
                response_builder = util.AudioController.play(response_builder, source, offset_in_ms)
        return (response_builder.response)

 
 
class PlayCommandHandler(AbstractRequestHandler):
    """Handler for Play command from hardware buttons or touch control.
    This handler handles the play command sent through hardware buttons such
    as remote control or the play control from Alexa-devices with a screen.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("PlaybackController.PlayCommandIssued")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        #session_attr = handler_input.attributes_manager.session_attributes
        if handler_input.request_envelope.context.audio_player is not None:
            if handler_input.request_envelope.context.audio_player.player_activity == PlayerActivity.STOPPED:
                source = handler_input.request_envelope.context.audio_player.token
                offset_in_ms = handler_input.request_envelope.context.audio_player.offset_in_milliseconds
                response_builder = util.AudioController.play(response_builder, source, offset_in_ms)
                access_token = get_account_linking_access_token(handler_input)
                user_email = util.get_user_profile(access_token, user_info = 'email')
                user_activity_log = {'Activity': 'PlayAudio', 'Status': 'touch'}
                util.log_user_activity_DB(user_email, user_activity_log)
        return (response_builder.response)
            
class PauseCommandHandler(AbstractRequestHandler):
    """Handler for Pause command from hardware buttons or touch control.
    This handler handles the pause command sent through hardware
    buttons such as remote control or the pause control from
    Alexa-devices with a screen.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("PlaybackController.PauseCommandIssued")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        #session_attr = handler_input.attributes_manager.session_attributes
        offset_in_ms = handler_input.request_envelope.context.audio_player.offset_in_milliseconds
        access_token = get_account_linking_access_token(handler_input)
        user_email = util.get_user_profile(access_token, user_info = 'email')
        user_activity_log = {'Activity': 'PauseAudio', 'Status': 'touch'}
        util.log_user_activity_DB(user_email, user_activity_log)
        #user_activity_log = {'Activity': 'PauseAudioButton', 'Status': 'true'}
        #util.log_user_activity_DB(session_attr['user_email'], user_activity_log)
        response_builder = util.AudioController.stop(response_builder)
        return (response_builder.response)



# ########## AUDIOPLAYER INTERFACE HANDLERS #########################
# This section contains handlers related to Audioplayer interface
# These handler does not matter at all. They are put here just to prevent CloudWatch from 
# generating errors. 

class PlaybackStartedHandler(AbstractRequestHandler):
    """AudioPlayer.PlaybackStarted Directive received.
    Confirming that the requested audio file began playing.
    Do not send any specific response.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("AudioPlayer.PlaybackStarted")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In PlaybackStartedHandler")
        logger.info("Playback started")
        return handler_input.response_builder.response

class PlaybackFinishedHandler(AbstractRequestHandler):
    """AudioPlayer.PlaybackFinished Directive received.
    Confirming that the requested audio file completed playing.
    Do not send any specific response.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("AudioPlayer.PlaybackFinished")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In PlaybackFinishedHandler")
        logger.info("Playback finished")
        return handler_input.response_builder.response


class PlaybackPausedHandler(AbstractRequestHandler):
    """AudioPlayer.PlaybackStopped Directive received.
    Confirming that the requested audio file stopped playing.
    Do not send any specific response.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("AudioPlayer.PlaybackPaused")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In PlaybackPausedHandler")
        logger.info("Playback paused")
        #print (handler_input.request_envelope.request)
        return handler_input.response_builder.response


class PlaybackStoppedHandler(AbstractRequestHandler):
    """AudioPlayer.PlaybackStopped Directive received.
    Confirming that the requested audio file stopped playing.
    Do not send any specific response.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("AudioPlayer.PlaybackStopped")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In PlaybackStoppedHandler")
        logger.info("Playback stopped")
        #print (handler_input.request_envelope.request)
        return handler_input.response_builder.response


class PlaybackNearlyFinishedHandler(AbstractRequestHandler):
    """AudioPlayer.PlaybackNearlyFinished Directive received.
    Replacing queue with the URL again. This should not happen on live streams.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("AudioPlayer.PlaybackNearlyFinished")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In PlaybackNearlyFinishedHandler")
        logger.info("Playback nearly finished")
        request = handler_input.request_envelope.request
        return handler_input.response_builder.response


class PlaybackFailedHandler(AbstractRequestHandler):
    """AudioPlayer.PlaybackFailed Directive received.
    Logging the error and restarting playing with no output speech and card.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("AudioPlayer.PlaybackFailed")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In PlaybackFailedHandler")
        request = handler_input.request_envelope.request
        logger.info("Playback failed: {}".format(request.error))
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        #user exit the skill in midway (i.e. has not confirmed the symptom level)
        access_token = get_account_linking_access_token(handler_input)
        user_email = util.get_user_profile(access_token, user_info = 'email')
        user_activity_log = {'Activity': 'ExitSkill', 'Status': 'true'}
        util.log_user_activity_DB(user_email, user_activity_log)
        speak_output = data.EXIT_VOICE
        return (
            handler_input.response_builder.set_should_end_session(True)
                .response
        )

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class YesNoIntentHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("YesNoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        response_builder = handler_input.response_builder
        slots = handler_input.request_envelope.request.intent.slots
        session_attr = handler_input.attributes_manager.session_attributes
        # user answers YES
        if (util.er_success_match(slots['yes_no'], slot_value='yes')):

            # user answer yes to the existence of metastases
            # ask where is the location of the metastases
            if session_attr['skill_state'] == "ask_metastases_question":
                speak_output = "Where are your bone metastases located? You can say torso or spine, or upper body, or lower body."
                response_builder = util.elicit_slot(response_builder, 
                                                slot_to_elicit = "location", 
                                                next_intent = "AskMetastasesLocationIntent")
                return response_builder.speak(speak_output).ask(speak_output).response  

            # user confirms the location of metastases
            # ask user to start nutrition topic of day
            elif session_attr['skill_state'] == "confirm_metastases_question":
                # store the location data into DynamoDB: 
                util.write_user_data_to_DynamoDB(table = dynamodb.Table('Nurse_AMIE_User_Progress_Status'), 
                            user_id = session_attr['user_email'], 
                            user_data = {'Activity': 'metastases_status', 'Status': session_attr['metastases_location']})
                session_attr['skill_state'] = "start_nutrition_topic_of_day"
                speak_output = "Thank you. Would you like to start today's activity?"
                # to avoid asking the intervention feedback on the first day of use         
                util.log_skill_state_DynamoDB(session_attr['user_email'], 
                                    skill_state = 'yesterday_intervention_feedback_ended')
                return response_builder.speak(speak_output).ask(speak_output).response  

            # user said the last time's intervention activity is helpful
            # respond with their feedback
            elif session_attr['skill_state'] == "ask_intervention_feedback":
                session_attr['intervention_feedback'] = 'positive'
                return RespondYesterdayInterventionFeedbackIntentHandler().handle(handler_input)
            
            # user agree to start topic of day
            elif session_attr['skill_state'] == "start_nutrition_topic_of_day":
                return TopicOfDayIntroIntentHandler().handle(handler_input)
            
            # the question is if user would like to REVIEW today's intervention activity
            elif session_attr['skill_state'] == "review_intervention_activity":
                return LoadInterventionMediaIntentHandler().handle(handler_input)

            # the question is whether user would like to start today's intervention activity by saying 'start intervention'
            # the following elif handles user's unexpected response. 
            elif session_attr['skill_state'] == "ask_user_symptom_question": 
                speak_output = 'If you would like to continue with today\'s intervention activity, say start intervention!'
                return response_builder.speak(speak_output).ask(speak_output).response
            
            # the question is wheather user confirms her symptom input
            elif session_attr['skill_state'] == "AskSymptomLevelIntent":
                return ConfirmSymptomLevelIntentHandler().handle(handler_input)
        elif (util.er_success_match(slots['yes_no'], slot_value='no')):
            
            # the question is whether yesterday's intervention is helpful
            if session_attr['skill_state'] == "ask_intervention_feedback":
                session_attr['intervention_feedback'] = 'negative'
                return RespondYesterdayInterventionFeedbackIntentHandler().handle(handler_input)

            # the question is whether user has metastases
            # user answered no bone metastases -> start daily routine activity. 
            elif session_attr['skill_state'] == "ask_metastases_question":
                util.write_user_data_to_DynamoDB(table = dynamodb.Table('Nurse_AMIE_User_Progress_Status'), 
                                            user_id = session_attr['user_email'], 
                                            user_data = {'Activity': 'metastases_status', 'Status': 'no met'})
                # to avoid asking the intervention feedback on the first day of use 
                util.log_skill_state_DynamoDB(session_attr['user_email'], 
                                    skill_state = 'yesterday_intervention_feedback_ended')
                session_attr['skill_state'] = "start_nutrition_topic_of_day"
                speak_output = "Ok. Would you like to start today\'s activity?'"
                return response_builder.speak(speak_output).ask(speak_output).response
            
            # user disagree on the location of bone metastases
            # ask the question again
            elif session_attr['skill_state'] == "confirm_metastases_question":
                speak_output = "You can say torso or spine, or upper body, or lower body."
                response_builder = util.elicit_slot(response_builder, 
                                                slot_to_elicit = "location", 
                                                next_intent = "AskMetastasesLocationIntent")
                return response_builder.speak(speak_output).ask(speak_output).response  
            else:
                return CancelOrStopIntentHandler().handle(handler_input)

        speak_output = "Sorry, I am not expecting a yes or no answer here."
        return response_builder.speak(speak_output).response



class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input) or 
                is_intent_name("GoodByeIntent")(handler_input) or 
                (is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and 
                list(handler_input.request_envelope.request.arguments)[0] == "exit_intervention"))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        response_builder = handler_input.response_builder
        response_builder = util.render_screen(response_builder, 
                            token = data.EXIT_TOKEN,
                            document = data.EXIT_DOCUMENT)
        skill_state = util.retrieve_same_day_skill_state(session_attr['user_email'])
        #user exit the skill in midway (i.e. has not confirmed the symptom level)
        if skill_state != 'intervention_activity_initated':
            speak_output = data.HALFWAY_EXIT_VOICE
        else:
            speak_output = data.EXIT_VOICE
        access_token = get_account_linking_access_token(handler_input)
        user_activity_log = {'Activity': 'StopSkill', 'Status': 'true'}
        util.log_user_activity_DB(session_attr['user_email'], user_activity_log)
        return (
            handler_input.response_builder
                .speak(speak_output).set_should_end_session(True)
                .response
        )


class PreviousIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.PreviousIntent")(handler_input) or 
                (is_request_type('Alexa.Presentation.APL.UserEvent')(handler_input) and 
                list(handler_input.request_envelope.request.arguments)[0] == "apl_back"))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        token = handler_input.request_envelope.context.alexa_presentation_apl.token
        session_attr = handler_input.attributes_manager.session_attributes
        util.log_intent_activity_DB(handler_input, session_attr, "AMAZON.PreviousIntent")
        if session_attr['skill_state'] == "PinkRibbonIntent":
            return HomeIntentHandler().handle(handler_input)
        elif ((session_attr['skill_state'] == "NutritionHomepageIntent") or 
                (session_attr['skill_state'] == "MovementsIntent") or
                (session_attr['skill_state'] == "CopingSymptomsIntent") or
                (session_attr['skill_state'] == "SoothingMusicIntent") or 
                (session_attr['skill_state'] == "GuidedRelaxationIntent")):
            return PinkRibbonIntentHandler().handle(handler_input)
        elif ((session_attr['skill_state'] == "LoadFavouriteRecipeListIntent") or
                (session_attr['skill_state'] == "LoadRecipeCategoryIntent") or 
                (session_attr['skill_state'] == "LoadRecipeIntroIntent_NewRecipe")):
            return NutritionHomepageIntentHandler().handle(handler_input)
        elif session_attr['skill_state'] == "LoadRecipeListByCategoryIntent":
            return LoadRecipeCategoryIntentHandler().handle(handler_input)
        elif session_attr['skill_state'] == "LoadRecipeIntroIntent_RecipeCategory":
            return LoadRecipeListByCategoryIntentHandler().handle(handler_input)
        elif session_attr['skill_state'] == "LoadRecipeIntroIntent_FavRecipe":
            return LoadFavouriteRecipeListIntentHandler().handle(handler_input)
        else:
            speak_output = "sorry, you can not return to the last page here."
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .response
            )




class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        session_attr = handler_input.attributes_manager.session_attributes
        # log the error message to s3
        speak_output = "Sorry, I had trouble doing what you asked. Please try again. "

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )



#sb = SkillBuilder()
sb = CustomSkillBuilder(api_client=DefaultApiClient())

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HomeIntentHandler())
sb.add_request_handler(PinkRibbonIntentHandler())
sb.add_request_handler(RespondYesterdayInterventionFeedbackIntentHandler())
sb.add_request_handler(AskExerciseLevelIntentHandler())
sb.add_request_handler(AskMetastasesLocationIntentHandler())
#sb.add_request_handler(LogInterventionFeedbackIntentHandler())

sb.add_request_handler(NutritionHomepageIntentHandler())
sb.add_request_handler(TopicOfDayIntroIntentHandler())
sb.add_request_handler(TopicOfDayMoreInfoIntentHandler())
sb.add_request_handler(LoadRecipeCategoryIntentHandler())
sb.add_request_handler(LoadRecipeListByCategoryIntentHandler())
sb.add_request_handler(LoadRecipeIntroIntentHandler())
sb.add_request_handler(LoadFavouriteRecipeListIntentHandler())
sb.add_request_handler(BookmarkRecipeIntentHandler())
sb.add_request_handler(LaunchRecipeURLIntentHandler())

sb.add_request_handler(MovementsIntentHandler())
sb.add_request_handler(CopingSymptomsIntentHandler())
sb.add_request_handler(GuidedRelaxationIntentHandler())
sb.add_request_handler(SoothingMusicIntentHandler())
sb.add_request_handler(PlayUserSelectedActivityIntentHandler())


sb.add_request_handler(YesNoIntentHandler())
sb.add_request_handler(AskSymptomLevelIntentHandler())
sb.add_request_handler(AskSymptomLevelIntentHandler())
sb.add_request_handler(ConfirmSymptomLevelIntentHandler())
sb.add_request_handler(PlayGetToFloorVideoIntentHandler())
#sb.add_request_handler(EndInterventionVideoIntentHandler())
sb.add_request_handler(ChangeGuidedActivityIntentHandler())
sb.add_request_handler(LoadInterventionMediaIntentHandler())
sb.add_request_handler(ResumeIntentHandler())
sb.add_request_handler(PauseIntentHandler())
sb.add_request_handler(PlayCommandHandler())
sb.add_request_handler(PauseCommandHandler())
#sb.add_request_handler(VideoControlButtonIntentHandler())
sb.add_request_handler(HelpIntentHandler())

sb.add_request_handler(PlaybackStartedHandler())
sb.add_request_handler(PlaybackFinishedHandler())
sb.add_request_handler(PlaybackStoppedHandler())
sb.add_request_handler(PlaybackPausedHandler())
sb.add_request_handler(PlaybackNearlyFinishedHandler())
sb.add_request_handler(PlaybackStartedHandler())
sb.add_request_handler(PlaybackFailedHandler())

sb.add_request_handler(YesNoIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(PreviousIntentHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())


def lambda_handler(event, context):
    print ("what are you returning")
    print (event)
    return sb.lambda_handler()(event, context)