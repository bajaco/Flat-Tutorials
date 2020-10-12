from . import db

# User class with linking id to auth0id
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    auth0_id = db.Column(db.String(600), nullable=False)
    unpublished = db.relationship('Unpublished_Tutorial')
    #published = db.relationship('Published_Tutorial')


    def __repr__(self):
        return '<User %r>' % str(self.id)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

# Association table between unpublished tutorials and tags
tutorial_tag = db.Table('tutorials_tags', db.Model.metadata,
        db.Column('left_id', db.Integer, db.ForeignKey('unpublished_tutorials.id')),
        db.Column('right_id', db.Integer, db.ForeignKey('tags.id'))
        )
# Unpublished tutorials, separately implemented from published
# tutorials so changes can be acccepted before publishing without
# causing the published tutorial to cease to be displayed
class Unpublished_Tutorial(db.Model):
    __tablename__ = 'unpublished_tutorials'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(), nullable=False)
    text = db.Column(db.String(), nullable=False)
    tags = db.relationship('Tag',
        secondary=tutorial_tag,
        back_populates='unpublished_tutorials')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

# Tags to be applied to tutorials when submitted
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    unpublished_tutorials = db.relationship(
        'Unpublished_Tutorial',
        secondary=tutorial_tag,
        back_populates='tags')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()



