from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ranobe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app, version='1.0', title='Ranobe Reader API',
    description='A simple Ranobe Reader API',
)

# Модели базы данных
class Ranobe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    chapters = db.relationship('Chapter', backref='ranobe', lazy=True)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ranobe_id = db.Column(db.Integer, db.ForeignKey('ranobe.id'), nullable=False)
    chapter_number = db.Column(db.Integer, nullable=False)
    content_ru = db.Column(db.Text)
    content_en = db.Column(db.Text)
    content_cn = db.Column(db.Text)

# Создание таблиц
with app.app_context():
    db.create_all()

# Модели Swagger
ranobe_model = api.model('Ranobe', {
    'id': fields.Integer(readonly=True, description='The ranobe unique identifier'),
    'title': fields.String(required=True, description='The ranobe title')
})

chapter_model = api.model('Chapter', {
    'id': fields.Integer(readonly=True, description='The chapter unique identifier'),
    'ranobe_id': fields.Integer(required=True, description='The ranobe ID'),
    'chapter_number': fields.Integer(required=True, description='The chapter number'),
    'content_ru': fields.String(description='The chapter content in Russian'),
    'content_en': fields.String(description='The chapter content in English'),
    'content_cn': fields.String(description='The chapter content in Chinese')
})

# Неймспейсы
ns_ranobe = api.namespace('ranobe', description='Ranobe operations')
ns_chapters = api.namespace('chapters', description='Chapter operations')

# Ranobe endpoints
@ns_ranobe.route('/')
class RanobeList(Resource):
    @ns_ranobe.doc('list_ranobe')
    @ns_ranobe.marshal_list_with(ranobe_model)
    def get(self):
        '''List all ranobe'''
        return Ranobe.query.all()

    @ns_ranobe.doc('create_ranobe')
    @ns_ranobe.expect(ranobe_model)
    @ns_ranobe.marshal_with(ranobe_model, code=201)
    def post(self):
        '''Create a new ranobe'''
        new_ranobe = Ranobe(title=api.payload['title'])
        db.session.add(new_ranobe)
        db.session.commit()
        return new_ranobe, 201

@ns_ranobe.route('/<int:id>')
@ns_ranobe.response(404, 'Ranobe not found')
@ns_ranobe.param('id', 'The ranobe identifier')
class RanobeItem(Resource):
    @ns_ranobe.doc('get_ranobe')
    @ns_ranobe.marshal_with(ranobe_model)
    def get(self, id):
        '''Fetch a ranobe given its identifier'''
        return Ranobe.query.get_or_404(id)

    @ns_ranobe.doc('update_ranobe')
    @ns_ranobe.expect(ranobe_model)
    @ns_ranobe.marshal_with(ranobe_model)
    def put(self, id):
        '''Update a ranobe given its identifier'''
        ranobe = Ranobe.query.get_or_404(id)
        ranobe.title = api.payload['title']
        db.session.commit()
        return ranobe

    @ns_ranobe.doc('delete_ranobe')
    @ns_ranobe.response(204, 'Ranobe deleted')
    def delete(self, id):
        '''Delete a ranobe given its identifier'''
        ranobe = Ranobe.query.get_or_404(id)
        db.session.delete(ranobe)
        db.session.commit()
        return '', 204

# Chapter endpoints
@ns_chapters.route('/')
class ChapterList(Resource):
    @ns_chapters.doc('create_chapter')
    @ns_chapters.expect(chapter_model)
    @ns_chapters.marshal_with(chapter_model, code=201)
    def post(self):
        '''Create a new chapter'''
        new_chapter = Chapter(
            ranobe_id=api.payload['ranobe_id'],
            chapter_number=api.payload['chapter_number'],
            content_ru=api.payload.get('content_ru', ''),
            content_en=api.payload.get('content_en', ''),
            content_cn=api.payload.get('content_cn', '')
        )
        db.session.add(new_chapter)
        db.session.commit()
        return new_chapter, 201

@ns_chapters.route('/<int:ranobe_id>/<int:chapter_number>')
@ns_chapters.response(404, 'Chapter not found')
@ns_chapters.param('ranobe_id', 'The ranobe identifier')
@ns_chapters.param('chapter_number', 'The chapter number')
@ns_chapters.param('lang', 'Language of the content (ru, en, cn). Default is ru')
class ChapterItem(Resource):
    @ns_chapters.doc('get_chapter')
    @ns_chapters.marshal_with(chapter_model)
    def get(self, ranobe_id, chapter_number):
        '''Fetch a chapter given its ranobe id and chapter number'''
        chapter = Chapter.query.filter_by(ranobe_id=ranobe_id, chapter_number=chapter_number).first_or_404()
        lang = request.args.get('lang', 'en')
        content_field = f'content_{lang}'
        if getattr(chapter, content_field):
            return chapter
        else:
            return {'error': f'Content not available in {lang}'}, 404

@ns_chapters.route('/<int:ranobe_id>/<int:chapter_number>/update_translation')
@ns_chapters.response(404, 'Chapter not found')
@ns_chapters.param('ranobe_id', 'The ranobe identifier')
@ns_chapters.param('chapter_number', 'The chapter number')
class ChapterTranslationUpdate(Resource):
    @ns_chapters.doc('update_chapter_translation')
    @ns_chapters.expect(api.model('TranslationUpdate', {
        'content_ru': fields.String(required=True, description='The updated Russian translation')
    }))
    @ns_chapters.marshal_with(chapter_model)
    def put(self, ranobe_id, chapter_number):
        '''Update the Russian translation of a chapter'''
        chapter = Chapter.query.filter_by(ranobe_id=ranobe_id, chapter_number=chapter_number).first_or_404()
        chapter.content_ru = api.payload['content_ru']
        db.session.commit()
        return chapter

if __name__ == '__main__':
    app.run(debug=True)
