import phonenumbers
from flask.ext.restful import Resource, request
from flask import jsonify

THROUGHPUT_SUBNET_MAP = {1: '10.0.1.0/24', 5: '10.0.2.0/24', 10: '10.0.3.0/24', 25: '10.0.4.0/24'}
SUPPORTED_COUNTRY_CODES = [1]
MESSAGE_PARAMETER = 'message'
RECIPIENTS_PARAMETER = 'recipients'
MAX_NUMBER_OF_RECIPIENTS = 5000


class Messages(Resource):
    def post(self):
        if MESSAGE_PARAMETER not in request.json.keys():
            response = jsonify(errorMessage='MESSAGE_PARAMETER_REQUIRED')
            response.status_code = 400
            return response

        if RECIPIENTS_PARAMETER not in request.json.keys():
            response = jsonify(errorMessage='RECIPIENTS_PARAMETER_REQUIRED')
            response.status_code = 400
            return response

        if request.json[MESSAGE_PARAMETER] is None:
            response = jsonify(errorMessage='MESSAGE_PARAMETER_CAN_NOT_BE_NONE')
            response.status_code = 400
            return response

        if request.json[RECIPIENTS_PARAMETER] is None:
            response = jsonify(errorMessage='RECIPIENTS_PARAMETER_CAN_NOT_BE_NONE')
            response.status_code = 400
            return response

        if len(request.json[RECIPIENTS_PARAMETER]) < 1:
            response = jsonify(errorMessage='RECIPIENTS_PARAMETER_SHOULD_HAVE_AT_LEAST_ONE_ITEM')
            response.status_code = 400
            return response

        if type(request.json[RECIPIENTS_PARAMETER]) != list:
            response = jsonify(errorMessage='RECIPIENTS_PARAMETER_SHOULD_BE_LIST')
            response.status_code = 400
            return response

        if len(request.json[RECIPIENTS_PARAMETER]) > len(set(request.json[RECIPIENTS_PARAMETER])):
            response = jsonify(errorMessage='RECIPIENTS_MUST_BE_UNIQUE')
            response.status_code = 400
            return response

        if len(request.json[RECIPIENTS_PARAMETER]) > MAX_NUMBER_OF_RECIPIENTS:
            response = jsonify(errorMessage=str(MAX_NUMBER_OF_RECIPIENTS) +'_RECIPIENTS_LIMIT_IS_EXCEEDED')
            response.status_code = 400
            return response

        errorMessage = self.validate_recipients(request.json[RECIPIENTS_PARAMETER])
        if len(errorMessage.keys()) > 1:
            response = jsonify(errorMessage=errorMessage)
            response.status_code = 400
            return response

        routes = self.get_routes(request.json[RECIPIENTS_PARAMETER])
        response = jsonify(message=request.json[MESSAGE_PARAMETER], routes=routes)
        response.status_code = 201
        return response

    def get_routes(self, recipients):
        routes = []

        for throughput in sorted(THROUGHPUT_SUBNET_MAP.keys(), reverse=True):
            requestsCount = len(recipients)/throughput
            for request in range(requestsCount):
                routes.append({'ip': THROUGHPUT_SUBNET_MAP[throughput].replace('0/24', str(request+1)),
                               'recipients': recipients[:throughput]})
                del recipients[:throughput]

        return routes

    def validate_recipients(self, recipients):
        errorMessage = {}

        for recipient in recipients:
            try:
                phoneNumber = phonenumbers.parse(recipient)

                if phoneNumber.country_code not in SUPPORTED_COUNTRY_CODES:
                    e = Exception()
                    e.message = 'NOT_US_PHONE_NUMBER'
                    raise e

                if not phonenumbers.is_valid_number(phoneNumber):
                    e = Exception()
                    e.message = 'NOT_VALID_US_PHONE_NUMBER'
                    raise e

            except Exception as e:
                errorMessageKey = e.message.replace(' ', '_').replace('.', '').upper()
                if errorMessageKey in errorMessage.keys():
                    errorMessage[errorMessageKey].append(recipient)
                else:
                    errorMessage[errorMessageKey] = [recipient]

        return errorMessage