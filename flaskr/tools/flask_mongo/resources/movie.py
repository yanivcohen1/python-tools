from mongoengine.queryset.visitor import Q
from flask import Response, request, jsonify
from database.models import Movie, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, MovieAlreadyExistsError, InternalServerError, \
UpdatingMovieError, DeletingMovieError, MovieNotExistsError
from app import app
from database.db import db
from .auth import admin_required


# not from restAPI
# @app.get('/test-app')
# @app.post('/test-app')
@app.route('/test-app', methods=['GET'])
def testApp():
    # return jsonify({'name': 'alice',
    #                'email': 'alice@outlook.com'})
    # query = Movie.objects()
    movies:list[Movie] = Movie.objects()
    print(movies[0].embeds[0].name) # yan1
    print(movies[1].embeds[0].name) # yan2
    return movies.to_json()

class MoviesApi(Resource):
    def get(self):
        query = Movie.objects()
        movies = Movie.objects().to_json()
        return Response(movies, mimetype="application/json", status=200)

    @jwt_required()
    def post(self):
        try:
            user_id = get_jwt_identity()
            # user_id = '637f3f586f953a55081b5c96'
            body = request.get_json()
            user:User = User.objects.get(id=user_id)
            movie =  Movie(**body, added_by=user)
            movie.save()
            user.update(push__movies=movie)
            user.save()
            id = movie.id
            return {'id': str(id)}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise MovieAlreadyExistsError
        except Exception as e:
            raise InternalServerError


class MovieApi(Resource):
    @jwt_required()
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            movie = Movie.objects.get(id=id, added_by=user_id)
            body = request.get_json()
            Movie.objects.get(id=id).update(**body)
            return '', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingMovieError
        except Exception:
            raise InternalServerError       
    
    @jwt_required()
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            movie:Movie = Movie.objects.get(id=id, added_by=user_id)
            movie.delete()
            return '', 200
        except DoesNotExist:
            raise DeletingMovieError
        except Exception:
            raise InternalServerError

    @admin_required()
    def get(self, id):
        try:
            movies = Movie.objects.get(id=id).to_json()
            return Response(movies, mimetype="application/json", status=200)
        except DoesNotExist:
            raise MovieNotExistsError
        except Exception:
            raise InternalServerError

class MoviesApiQuery(Resource): # /api/movie?name=yaniv5@gmail.com&name2=yan1&value=con1
    def get(self):
        name = request.args.get("name")
        name2 = request.args.get("name2")
        val = request.args.get("value")
        # find = Movie.objects(embeds__match={ "name": name, "value": val })
        # find = Movie.objects.filter( (Q(account=account) and Q(public=True)) or  (Q(account=account) and Q(creator=logged_in_user)) ).order_by('-last_used')
        find: Movie = Movie.objects.filter( (Q(name=name) and Q(embeds__name=name2)) or  
                                    (Q(name=name) and Q(embeds__value=val)) ).order_by('-name')
        # .skip( offset ).limit( items_per_page )
        movies = find.to_json()
        return Response(movies, mimetype="application/json", status=200)
        # advanced-queries
        # https://docs.mongoengine.org/guide/querying.html#advanced-queries
        # Get published posts
        # Post.objects(Q(published=True) | Q(publish_date__lte=datetime.now()))

        # Get top posts
        # Post.objects((Q(featured=True) & Q(hits__gte=1000)) | Q(hits__gte=5000))
        
        # pipeline = [
        #   {"$sort" : {"name" : -1}},
        #   {"$project": {"_id": 0, "name": {"$toUpper": "$name"}}}
        # ]
        # data = Person.objects().aggregate(pipeline)
