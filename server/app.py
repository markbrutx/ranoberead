from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import func

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type"]}}, support_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ranobe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app, version='1.0', title='Ranobe Reader API',
    description='A simple Ranobe Reader API',
)
migrate = Migrate(app, db)

# Модели базы данных
class Ranobe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    chapters = db.relationship('Chapter', backref='ranobe', lazy=True)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ranobe_id = db.Column(db.Integer, db.ForeignKey('ranobe.id'), nullable=False)
    chapter_id = db.Column(db.Integer, nullable=False)  # New field
    chapter_number_origin = db.Column(db.Integer, nullable=False)  # Renamed from chapter_number
    title_ru = db.Column(db.String(200))
    title_en = db.Column(db.String(200))
    content_ru = db.Column(db.Text)
    content_en = db.Column(db.Text)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ranobe_id = db.Column(db.Integer, db.ForeignKey('ranobe.id'), nullable=False)
    chapter_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    ranobe = db.relationship('Ranobe', backref=db.backref('bookmarks', lazy=True))

    __table_args__ = (db.UniqueConstraint('ranobe_id', name='uix_1'),)

# Создание таблиц
with app.app_context():
    db.create_all()

chapter_summary_model = api.model('ChapterSummary', {
    'id': fields.Integer(readonly=True, description='The chapter unique identifier'),
    'chapter_id': fields.Integer(description='The actual chapter ID'),
    'chapter_number_origin': fields.Integer(description='The original chapter number from the website'),
    'title_ru': fields.String(description='The chapter title in Russian'),
    'title_en': fields.String(description='The chapter title in English'),
    'content_preview_ru': fields.String(description='Preview of the Russian content'),
    'content_preview_en': fields.String(description='Preview of the English content')
})

# Модели Swagger
ranobe_model = api.model('Ranobe', {
    'id': fields.Integer(readonly=True, description='The ranobe unique identifier'),
    'title': fields.String(required=True, description='The ranobe title'),
    'chapters': fields.List(fields.Nested(chapter_summary_model), description='List of chapters')
})

chapter_model = api.model('Chapter', {
    'id': fields.Integer(readonly=True, description='The chapter unique identifier'),
    'ranobe_id': fields.Integer(required=True, description='The ranobe ID'),
    'chapter_id': fields.Integer(required=True, description='The actual chapter ID'),
    'chapter_number_origin': fields.Integer(required=True, description='The original chapter number from the website'),
    'title_ru': fields.String(description='The chapter title in Russian'),
    'title_en': fields.String(description='The chapter title in English'),
    'content_ru': fields.String(description='The chapter content in Russian'),
    'content_en': fields.String(description='The chapter content in English'),
})

ranobe_list_model = api.model('RanobeList', {
    'id': fields.Integer(readonly=True, description='The ranobe unique identifier'),
    'title': fields.String(required=True, description='The ranobe title'),
    'chapter_count': fields.Integer(description='Number of chapters in the ranobe')
})

ranobe_create_model = api.model('RanobeCreate', {
    'title': fields.String(required=True, description='The ranobe title')
})

ranobe_detail_model = api.model('RanobeDetail', {
    'id': fields.Integer(readonly=True, description='The ranobe unique identifier'),
    'title': fields.String(required=True, description='The ranobe title'),
    'chapter_count': fields.Integer(description='Number of chapters in the ranobe'),
    'chapters': fields.List(fields.Nested(chapter_summary_model), description='List of chapters')
})

bookmark_model = api.model('Bookmark', {
    'id': fields.Integer(readonly=True, description='The bookmark unique identifier'),
    'ranobe_id': fields.Integer(required=True, description='The ranobe ID'),
    'chapter_id': fields.Integer(required=True, description='The chapter ID'),
    'ranobe_title': fields.String(description='The ranobe title'),
    'chapter_title_ru': fields.String(description='The chapter title in Russian'),
    'chapter_number_origin': fields.Integer(description='The original chapter number')
})

# Неймспейсы
ns_ranobe = api.namespace('ranobe', description='Ranobe operations')
ns_chapters = api.namespace('chapters', description='Chapter operations')
ns_bookmarks = api.namespace('bookmarks', description='Bookmark operations')

# Ranobe endpoints
@ns_ranobe.route('/')
class RanobeList(Resource):
    @ns_ranobe.doc('list_ranobe')
    @ns_ranobe.marshal_list_with(ranobe_list_model)
    def get(self):
        '''List all ranobe with their title, ID, and chapter count'''
        ranobe_list = db.session.query(
            Ranobe.id, 
            Ranobe.title, 
            func.count(Chapter.id).label('chapter_count')
        ).outerjoin(Chapter).group_by(Ranobe.id).all()

        return [
            {
                'id': ranobe.id,
                'title': ranobe.title,
                'chapter_count': ranobe.chapter_count
            } for ranobe in ranobe_list
        ]

    @ns_ranobe.doc('create_ranobe')
    @ns_ranobe.expect(ranobe_create_model)
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
class RanobeView(Resource):
    @ns_ranobe.doc('get_ranobe')
    @ns_ranobe.marshal_with(ranobe_detail_model)
    def get(self, id):
        '''Get all details about a specific ranobe'''
        ranobe = Ranobe.query.get_or_404(id)
        
        chapters = Chapter.query.filter_by(ranobe_id=id).order_by(Chapter.chapter_number_origin).all()
        
        def get_content_preview(content, max_length=100):
            if content:
                return content[:max_length] + ('...' if len(content) > max_length else '')
            return None
        
        return {
            'id': ranobe.id,
            'title': ranobe.title,
            'chapter_count': len(chapters),
            'chapters': [{
                'id': chapter.id,
                'chapter_id': chapter.chapter_id,
                'chapter_number_origin': chapter.chapter_number_origin,
                'title_ru': chapter.title_ru,
                'title_en': chapter.title_en,
                'content_preview_ru': get_content_preview(chapter.content_ru),
                'content_preview_en': get_content_preview(chapter.content_en)
            } for chapter in chapters]
        }

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

@ns_chapters.route('/')
class ChapterList(Resource):
    @ns_chapters.doc('create_chapter')
    @ns_chapters.expect(chapter_model)
    @ns_chapters.marshal_with(chapter_model, code=201)
    def post(self):
        '''Create a new chapter or update if exists'''
        data = api.payload
        chapter = Chapter.query.filter_by(ranobe_id=data['ranobe_id'], chapter_id=data['chapter_id']).first()
        
        if chapter:
            # Update existing chapter
            for key, value in data.items():
                if hasattr(chapter, key) and value is not None:
                    setattr(chapter, key, value)
        else:
            # Create new chapter
            chapter = Chapter(**data)
            db.session.add(chapter)
        
        db.session.commit()
        return chapter, 201

@ns_chapters.route('/<int:ranobe_id>/<int:chapter_id>')
@ns_chapters.response(404, 'Chapter not found')
@ns_chapters.param('ranobe_id', 'The ranobe identifier')
@ns_chapters.param('chapter_id', 'The actual chapter ID')
@ns_chapters.param('lang', 'Language of the content (ru, en, cn). Default is ru')
class ChapterItem(Resource):
    @ns_chapters.doc('get_chapter')
    @ns_chapters.marshal_with(chapter_model)
    def get(self, ranobe_id, chapter_id):
        '''Fetch a chapter given its ranobe id and chapter id'''
        chapter = Chapter.query.filter_by(ranobe_id=ranobe_id, chapter_id=chapter_id).first_or_404()
        lang = request.args.get('lang', 'en')
        
        response = {
            'id': chapter.id,
            'ranobe_id': chapter.ranobe_id,
            'chapter_id': chapter.chapter_id,
            'chapter_number_origin': chapter.chapter_number_origin,
            'title_ru': chapter.title_ru,
            'title_en': chapter.title_en,
        }
        
        content_field = f'content_{lang}'
        if hasattr(chapter, content_field) and getattr(chapter, content_field):
            response[content_field] = getattr(chapter, content_field)
            return response
        else:
            return {'error': f'Content not available in {lang}'}, 404

@ns_chapters.route('/<int:ranobe_id>/<int:chapter_id>/update_translation')
@ns_chapters.response(404, 'Chapter not found')
@ns_chapters.param('ranobe_id', 'The ranobe identifier')
@ns_chapters.param('chapter_id', 'The actual chapter ID')
class ChapterTranslationUpdate(Resource):
    @ns_chapters.doc('update_chapter_translation')
    @ns_chapters.expect(api.model('TranslationUpdate', {
        'content_ru': fields.String(description='The updated Russian translation content'),
        'title_ru': fields.String(description='The updated Russian translation title')
    }))
    @ns_chapters.marshal_with(chapter_model)
    def put(self, ranobe_id, chapter_id):
        '''Update the Russian translation of a chapter (content and/or title)'''
        chapter = Chapter.query.filter_by(ranobe_id=ranobe_id, chapter_id=chapter_id).first_or_404()
        
        if 'content_ru' in api.payload:
            chapter.content_ru = api.payload['content_ru']
        
        if 'title_ru' in api.payload:
            chapter.title_ru = api.payload['title_ru']
        
        db.session.commit()
        return chapter

@ns_bookmarks.route('/')
class BookmarkList(Resource):
    @ns_bookmarks.doc('list_bookmarks')
    @ns_bookmarks.marshal_list_with(bookmark_model)
    def get(self):
        '''List all bookmarks'''
        bookmarks = db.session.query(
            Bookmark,
            Ranobe.title.label('ranobe_title'),
            Chapter.title_ru.label('chapter_title_ru'),
            Chapter.chapter_number_origin
        ).join(Ranobe, Bookmark.ranobe_id == Ranobe.id)\
         .join(Chapter, (Chapter.ranobe_id == Bookmark.ranobe_id) & 
                        (Chapter.chapter_id == Bookmark.chapter_id))\
         .all()

        return [{
            'id': bookmark.Bookmark.id,
            'ranobe_id': bookmark.Bookmark.ranobe_id,
            'chapter_id': bookmark.Bookmark.chapter_id,
            'ranobe_title': bookmark.ranobe_title,
            'chapter_title_ru': bookmark.chapter_title_ru,
            'chapter_number_origin': bookmark.chapter_number_origin
        } for bookmark in bookmarks]

    @ns_bookmarks.doc('create_or_update_bookmark')
    @ns_bookmarks.expect(api.model('BookmarkCreate', {
        'ranobe_id': fields.Integer(required=True, description='The ranobe ID'),
        'chapter_id': fields.Integer(required=True, description='The chapter ID')
    }))
    @ns_bookmarks.marshal_with(bookmark_model, code=201)
    def post(self):
        '''Create a new bookmark or update existing one for the ranobe'''
        data = api.payload
        
        # Check if a bookmark for this ranobe already exists
        existing_bookmark = Bookmark.query.filter_by(ranobe_id=data['ranobe_id']).first()
        
        if existing_bookmark:
            # Update existing bookmark
            existing_bookmark.chapter_id = data['chapter_id']
            db.session.commit()
            bookmark = existing_bookmark
        else:
            # Create new bookmark
            new_bookmark = Bookmark(ranobe_id=data['ranobe_id'], chapter_id=data['chapter_id'])
            db.session.add(new_bookmark)
            db.session.commit()
            bookmark = new_bookmark
        
        # Fetch additional data for response
        bookmark_data = db.session.query(
            Bookmark,
            Ranobe.title.label('ranobe_title'),
            Chapter.title_ru.label('chapter_title_ru'),
            Chapter.chapter_number_origin
        ).join(Ranobe, Bookmark.ranobe_id == Ranobe.id)\
         .join(Chapter, (Chapter.ranobe_id == Bookmark.ranobe_id) & 
                        (Chapter.chapter_id == Bookmark.chapter_id))\
         .filter(Bookmark.id == bookmark.id).first()

        return {
            'id': bookmark_data.Bookmark.id,
            'ranobe_id': bookmark_data.Bookmark.ranobe_id,
            'chapter_id': bookmark_data.Bookmark.chapter_id,
            'ranobe_title': bookmark_data.ranobe_title,
            'chapter_title_ru': bookmark_data.chapter_title_ru,
            'chapter_number_origin': bookmark_data.chapter_number_origin
        }, 201
        
@app.route('/bookmarks', methods=['OPTIONS'])
def options():
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
