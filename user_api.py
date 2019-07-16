import json


from app.db.user import User
from flask_restful import Resource, abort
from flask import request
from datetime import datetime, time
from app.flask_app import api


class MyJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, User):
            return obj.to_json()

        return json.JSONEncoder.default(self, obj)


class UserApi(Resource):
    def get(self):
        users = User.query_all()
        # return json.dumps(users[0], cls=MyJsonEncoder)
        # return {
        #     'status': 'ok',
        #     'data:': [
        #         x.to_json() for x in users
        #     ]
        # }
        return [x.to_json() for x in users]

    def post(self):
        json_data = request.get_json()
        if not json_data:
            print('No data in this post. aborting')
            abort(400)

        username = json_data['username']
        age = int(json_data['age'])
        birthday = datetime.strptime(json_data['birthday'], "%Y-%m-%d")

        if not username or not age or not birthday:
            print("API-Create-post: Username or age or birthday missing")
            abort(400)
        if User.query_single_by_username(username):
            print("API-Create-post: Username already exists")
            abort(500)

        user = User(
            username=username,
            age=age,
            birthday=birthday
        )
        print(user)
        user.put()
        return user.to_json()

    def put(self):

        json_data = request.get_json()
        if not json_data:
            print('No data in this post. aborting')
            abort(400)

        username_old = json_data['username_old']
        age_old = int(json_data['age_old'])
        birthday_old = datetime.strptime(json_data['birthday_old'], "%Y-%m-%d")

        username_new = json_data['username_new']
        age_new = int(json_data['age_new'])
        birthday_new = datetime.strptime(json_data['birthday_new'], "%Y-%m-%d")

        user = User.query_single_by_username(username_old)
        if not user:
            print("UPDATE_ENTITY: User not found")
            abort(400)

        user.username = username_new
        user.age = age_new
        user.birthday = birthday_new

        user.put()

        return user.to_json()


    def delete(self):
        username = request.headers["username"]
        if not username:
            print('No data in this post. aborting')
            abort(400)
        print username
        user = User.query_single_by_username(username)
        if not user:
            print "User does not exist"
            abort(400)
        user.key.delete()
        return {}, 204



api.add_resource(UserApi, '/v1/user')
