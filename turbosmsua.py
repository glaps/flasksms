# -*- coding: utf-8 -*-
from suds.client import Client
proxy={}

class Turbosms:

    def __init__(self, login, password):
        self.client = Client('http://turbosms.in.ua/api/wsdl.html',proxy=proxy)
        auth_result = self.client.service.Auth(login, password)

        if auth_result != "Вы успешно авторизировались":
            raise ValueError("Auth error: %s" % auth_result)

    def balance(self):
        balance_result = self.client.service.GetCreditBalance()

        try:
            balance = float(balance_result)
        except ValueError:
            raise ValueError("Balance error: %s" % balance_result)

        return balance

    def send_text(self, sender, destinations, text, wappush=False):
        if not type(destinations) is list:
            destinations = [destinations]

        def format_destination(d):
            d = str(d)
            if len(d) == 9:
                return "+380%s" % d
            if len(d) == 10:
                return "+38%s" % d
            if len(d) == 11:
                return "+3%s" % d
            if len(d) == 12:
                return "+%s" % d
            if len(d) == 13:
                return d
            raise Exception("Invalid destination: %s" % d)

        destinations_formated = ",".join(map(format_destination, destinations))

        if not wappush:
            send_result = self.client.service.SendSMS(sender, destinations_formated, text).ResultArray
        else:
            send_result = self.client.service.SendSMS(sender, destinations_formated, text, wappush).ResultArray

        send_status = send_result.pop(0)

        to_return = {"status": send_status}
        for i, sms_id in enumerate(send_result):
            to_return[destinations[i]] = sms_id

        return to_return

    def message_status(self, message_id):
        status = self.client.service.GetMessageStatus(message_id)
        return status
