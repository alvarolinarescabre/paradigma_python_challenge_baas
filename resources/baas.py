from flask import jsonify, abort
from flask_restful import Resource, reqparse, fields, marshal
import urllib
import json

class Place(Resource):
    def get(self):
        place = urllib.request.urlopen('http://place:8081/v1/places')
        string_place = place.read().decode('utf-8')
        json_place = json.loads(string_place)
        
        people = urllib.request.urlopen('http://people:8082/v1/people')
        string_people = people.read().decode('utf-8')
        json_people = json.loads(string_people)
        
        data = []
        i = 0
        
        for place in json_place:
            data.append({'id': place['id'], 'name': place['name'], 'people': [] })
            for people in json_people:
                if place['id'] == people['place_id']:
                    data[i]['people'].append({ 'id': people['id'], 'name': people['name'], 'is_king': people['is_king'], 'is_alive': people['is_alive'] })
            i += 1
                    
        return data

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required = True)
        args = parser.parse_args()

        try:
            data = json.dumps(args).encode('utf8')
            request = urllib.request.Request(url='http://place:8081/v1/places', data=data, headers={'Content-type': 'application/json'}, method='POST')
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            status_code = e.code
            
            if status_code == 409:
                abort(409, 'Conflict')
            elif status_code == 400:
                abort(400, 'Bad Request')
            else:
                abort(500, 'Internal Server Error')

        if response:
            return json.dumps({'success':True}), 201, {'ContentType':'application/json'} 
        else:
            abort(400, 'Bad Request')
    
class PlaceById(Resource):
    def get(self, id):
        if id is None:
                   abort(400, 'Bad Request')
        else:
            try:
                place = urllib.request.urlopen('http://place:8081/v1/places/{}'.format(id))
                string_place = place.read().decode('utf-8')
                json_place = json.loads(string_place)
            
                people = urllib.request.urlopen('http://people:8082/v1/people')
                string_people = people.read().decode('utf-8')
                json_people = json.loads(string_people)
                
            except urllib.error.HTTPError:
                abort(404, 'Not Found')
            
        data = []
        i = 0
        
        for place in json_place:
            data.append({'id': place['id'], 'name': place['name'], 'people': [] })
            for people in json_people:
                if place['id'] == people['place_id']:
                    data[i]['people'].append({ 'id': people['id'], 'name': people['name'], 'is_king': people['is_king'], 'is_alive': people['is_alive'] })
            i += 1
                    
        return data

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='view_args', required = True)
        parser.add_argument('name', location='json', required = True)
        args = parser.parse_args()

        if args['id'] is None:
               abort(400, 'Bad Request')
        else:
            try:
                data = json.dumps(args).encode('utf8')
                request = urllib.request.Request(url='http://place:8081/v1/places/{}'.format(id), data=data, headers={'Content-type': 'application/json'}, method='PUT')
                response = urllib.request.urlopen(request)
            except urllib.error.HTTPError as e:
                status_code = e.code
                
                if status_code == 409:
                    abort(409, 'Conflict')
                elif status_code == 400:
                    abort(400, 'Bad Request')
                else:
                    abort(500, 'Internal Server Error')

        if response:
            return json.dumps({'success':True}), 201, {'ContentType':'application/json'} 
        else:
            abort(400, 'Bad Request')
            
    def delete(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='view_args', required = True)
        args = parser.parse_args()
            
        place = PlaceById.get(self,args['id'])

        if place[0]['people'] == []:
            try:
                data = json.dumps(args).encode('utf8')
                request = urllib.request.Request(url='http://place:8081/v1/places/{}'.format(id), data=data, headers={'Content-type': 'application/json'}, method='DELETE')
                response = urllib.request.urlopen(request)
            except urllib.error.HTTPError as e:
                status_code = e.code
            
                if status_code == 400:
                    abort(400, 'Bad Request')
                else:
                    abort(500, 'Internal Server Error')
        elif place[0]['people'] != []:                
            for king in place[0]['people']:        
                if king['is_alive'] is False and king['is_king'] is False :
                    try:
                        data = json.dumps(args).encode('utf8')
                        request = urllib.request.Request(url='http://place:8081/v1/places/{}'.format(id), data=data, headers={'Content-type': 'application/json'}, method='DELETE')
                        response = urllib.request.urlopen(request)
                    except urllib.error.HTTPError as e:
                        status_code = e.code
                    
                        if status_code == 400:
                            abort(400, 'Bad Request')
                        else:
                            abort(500, 'Internal Server Error')
                else:
                    return abort(403, 'Forbidden')
        
        if response:
            return json.dumps({'success':True}), 201, {'ContentType':'application/json'} 
        else:
            abort(400, 'Bad Request')

class People(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required = True)
        parser.add_argument('is_alive', location='json', required = True)
        parser.add_argument('is_king', location='json', required = True)
        parser.add_argument('place_id', location='json', required = True)

        args = parser.parse_args()
        args['is_alive'] = 1
        
        place = PlaceById.get(self, args['place_id'])

        if place[0]['people'] == []:
            try:
                data = json.dumps(args).encode('utf8')
                request = urllib.request.Request(url='http://people:8082/v1/people', data=data, headers={'Content-type': 'application/json'}, method='POST')
                response = urllib.request.urlopen(request)
            except urllib.error.HTTPError as e:
                status_code = e.code
            
                if status_code == 400:
                    abort(400, 'Bad Request')
                else:
                    abort(409, 'Conflict')


        for people in place:
            for i in range(0, len(people['people'])):
                if args['is_king'] == '1' and people['people'][i]['is_king'] is True:
                    abort(409, 'Conflict')
                else:
                    try:
                        data = json.dumps(args).encode('utf8')
                        request = urllib.request.Request(url='http://people:8082/v1/people', data=data, headers={'Content-type': 'application/json'}, method='POST')
                        response = urllib.request.urlopen(request)
                        break
                    except urllib.error.HTTPError as e:
                        status_code = e.code
                        
                        if status_code == 409:
                            abort(409, 'Conflict')
                        elif status_code == 400:
                            abort(400, 'Bad Request')
                        else:
                            abort(500, 'Internal Server Error')

        if response:
            return json.dumps({'success':True}), 201, {'ContentType':'application/json'} 
        else:
            abort(400, 'Bad Request')

class PeopleById(Resource):
    def put(self, id):       
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='view_args', required = True)
        parser.add_argument('name', location='json', required = True)
        parser.add_argument('is_alive', location='json', required = True)
        parser.add_argument('is_king', location='json', required = True)
        parser.add_argument('place_id', location='json', required = True)
        args = parser.parse_args()

        data = json.dumps(args).encode('utf8')

        place = PlaceById.get(self, args['place_id'])

        for people in place:
            for i in range(0, len(people['people'])):
                if args['is_king'] == '1' and people['people'][i]['is_king'] is True:
                    abort(409, 'Conflict')
                else:
                    try:
                        data = json.dumps(args).encode('utf8')
                        request = urllib.request.Request(url='http://people:8082/v1/people/{}'.format(id), data=data, headers={'Content-type': 'application/json'}, method='PUT')
                        response = urllib.request.urlopen(request)
                        break
                    except urllib.error.HTTPError as e:
                        status_code = e.code
                        
                        if status_code == 409:
                            abort(409, 'Conflict')
                        elif status_code == 400:
                            abort(400, 'Bad Request')
                        else:
                            abort(500, 'Not Found')

        if response:
            return json.dumps({'success':True}), 201, {'ContentType':'application/json'} 
        else:
            abort(400, 'Bad Request')
            
    def delete(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='view_args', required = True)
        args = parser.parse_args()

        try:
            request = urllib.request.Request(url='http://people:8082/v1/people/{}'.format(id), headers={'Content-type': 'application/json'}, method='DELETE')
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            status_code = e.code
            
            if status_code == 400:
                abort(400, 'Bad Request')
            else:
                abort(404, 'Not Found')
        
        if response:
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
        else:
            abort(404, 'Not Found')
