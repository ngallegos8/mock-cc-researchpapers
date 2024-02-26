#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Research, Author, ResearchAuthors

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

class ResearchAll(Resource):

    def get(self):
        
        researches = [r.to_dict() for r in Research.query.all()]
        return researches, 200
    
api.add_resource(ResearchAll, '/research')


class ResearchByID(Resource):

    def get(self, id):
        research = Research.query.filter(Research.id==id).first()
        if research:
            return research.to_dict(),200
        else:
            return {"error": "Research paper not found"}, 400
        
    def delete(self,id):
        research = Research.query.filter(Research.id==id).first()
        if research:
            db.session.delete(research)
            db.session.commit()
            return {}, 200
        else:
            return {"error": "Research paper not found"}, 400

api.add_resource(ResearchByID, '/research/<int:id>')

class AuthorAll(Resource):
    def get(self):
        authors = [author.to_dict() for author in Author.query.all()]
        for author in authors:
            authors.append(author.to_dict(rules = ('-researchauthors')))
        return authors, 200
    
api.add_resource(AuthorAll, '/authors')


class ResearchAuthorsRoute(Resource):
    def post(self):
        data = request.get_json()
        try:
            research_authors = ResearchAuthors(
                author_id = data["author_id"],
                research_id = data["research_id"]
            )
            db.session.add(research_authors)
            db.session.commit()
            return research_authors.to_dict(), 201
        except:
            return {"errors": ["validation errors"]}, 400

api.add_resource(ResearchAuthorsRoute, '/research_author')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
