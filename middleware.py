from flask import Flask, request, abort
import requests

class Middleware():
    def validateAccessToken(token):
        try:
            url = "http://homeassistant.local:8123/api/"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": str(token)
            }
            print(request.authorization)
            response = requests.get(url, headers=headers)
            print(response)

            if response.status_code == 200:
                return True

            else:
                return False

        except Exception as e:
            return {"Invalid access token": str(e)}, 401
        
    