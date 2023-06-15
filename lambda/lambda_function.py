# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

import os
from statistics import mean
from collections import defaultdict
from locations import Location_Breakdown
from concurrent.futures import ThreadPoolExecutor, as_completed
from nautical.io import create_buoy


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# basic search criteria and reported data.
_search_data = {
    "wvht": ["wave height", "feet"],
    "apd": ["period", "seconds"],
    "wtmp": ["water temperature", "degrees"]
}

def _create_buoy(buoy_id):
    buoy = create_buoy(buoy_id)
    
    pulled_data = {}
    if buoy is not None:
        pulled_data = {key: getattr(buoy.data, key) for key in _search_data if getattr(buoy.data, key) is not None}
    
    return pulled_data


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to nautical data, you can ask for information about buoys or say Help. Which would you like to try?"
        reprompt = "I did not understand that request. Would you like information about buoys?"
        logger.info("Handling Launch")

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
        )


class BuoyIntentHandler(AbstractRequestHandler):
    """Handler to provide information about a specific buoy.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("Buoy")(handler_input)

    def handle(self, handler_input):
        buoy_id = handler_input.request_envelope.request.intent.slots["buoy_id"].value
        
        pulled_data = _create_buoy(buoy_id)
        if pulled_data:
            speak_output = ", ".join([f"{_search_data[key][0]} is {value} {_search_data[key][1]}" for key, value in pulled_data.items()])
        else:
            speak_output = f"I was not able to find data for {buoy_id}"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class BuoysNearLocationIntentHandler(AbstractRequestHandler):
    """Handler to provide buoys that can be found close to a
    specific city/state location.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("BuoysNearLocation")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        city = handler_input.request_envelope.request.intent.slots["near_city"].value
        state = handler_input.request_envelope.request.intent.slots["near_state"].value
        
        try:
            buoys = Location_Breakdown[state.lower()][city.lower()]["names"]
            buoy_str = ", ".join(buoys)
            speak_output = f"I found the following buoys. {buoy_str}"
        except KeyError as e:
            speak_output = f"I could not find buoys in {city} {state}"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class DataNearLocationIntentHandler(AbstractRequestHandler):
    """Handler to provide information about buoys that can be found close to a
    specific city/state location.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DataNearLocation")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        city = handler_input.request_envelope.request.intent.slots["near_city"].value
        state = handler_input.request_envelope.request.intent.slots["near_state"].value

        speak_output = ""
        
        try:
            buoys = Location_Breakdown[state.lower()][city.lower()]["buoys"]
            averages = defaultdict(list)
            with ThreadPoolExecutor(max_workers=10) as executor:
                find_buoy_data = {executor.submit(_create_buoy, buoy_id): 
                    buoy_id for buoy_id in buoys}
                
                for futr in as_completed(find_buoy_data):
                    for key, value in futr.result().items():
                        averages[key].append(float(value))
                if averages:
                    speak_output = ", ".join([f"the average {_search_data[key][0]} is {round(mean(value), 2)} {_search_data[key][1]}" for key, value in averages.items()])
        except KeyError as e:
            speak_output = f"I could not find buoys in {city} {state}"
            
        if not speak_output:
            speak_output = f"I was unable to retrieve data for {city} {state}"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You may ask for the report for a specific buoy," \
            "list buoy data near city and state, " \
                "or list my buoy data."
        logger.info("Handling help")

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.
        logger.info("Handling Session End")
        return handler_input.response_builder.response


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

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(BuoyIntentHandler())
sb.add_request_handler(BuoysNearLocationIntentHandler())
sb.add_request_handler(DataNearLocationIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()