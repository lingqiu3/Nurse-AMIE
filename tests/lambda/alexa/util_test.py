from unittest import mock
import requests

# the import statement fails given "lambda" is a keyword
_temp = __import__("lambda.alexa", fromlist=["data", "util"])
util = _temp.util
data = _temp.data


def test_send_data_external_api():
    session_attr = {
        "user_email": "a@example.com",
        "sleep_value": "5",
        "fatigue_value": "4",
        "distress_value": "2",
        "pain_value": "8",
        "steps_value": "1200",
        "intervention_category": "intervention_2",
        "intervention_title": "Intervention_title",
        "login_time": "1600392606",
    }

    expected = {
        "UserId": session_attr["user_email"],
        "Questions": [
            {"type": "sleep", "value": session_attr["sleep_value"]},
            {"type": "fatigue", "value": session_attr["fatigue_value"]},
            {"type": "distress", "value": session_attr["distress_value"]},
            {"type": "pain", "value": session_attr["pain_value"]},
            {"type": "steps", "value": session_attr["steps_value"]},
        ],
        "InterventionType:": session_attr["intervention_category"],
        "Intervention": session_attr["intervention_title"],
        "InTime": session_attr["login_time"],
    }

    with mock.patch("requests.post") as m:
        util.send_data_external_api(session_attr)
        m.assert_called_once_with(data.DASH_BOARD_POST_URL, json=expected)

    # exceptions should be handled
    with mock.patch("requests.post", side_effect=requests.exceptions.HTTPError) as m:
        util.send_data_external_api(session_attr)

    # actual call
    temp = data.DASH_BOARD_POST_URL
    data.DASH_BOARD_POST_URL = "https://dashboard.test"
    util.send_data_external_api(session_attr)
    data.DASH_BOARD_POST_URL = temp
