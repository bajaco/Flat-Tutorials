from . import db

# Helper functions

def dictit(obj, *args):
    new_dict = {}
    for arg in args:
        result = getattr(obj, arg)
        if isinstance(result,list):
            result = [str(i) for i in result]
        elif isinstance(result,int):
            result = result
        else:
            result = str(result)

        new_dict[arg] = result
        
    return new_dict


# User class with linking id to auth0id
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    auth0_id = db.Column(db.String(600), nullable=False)
    username = db.Column(db.String(20))
    unpublished = db.relationship('Unpublished_Tutorial',
            backref='author',
            lazy=True)
    published = db.relationship('Published_Tutorial',
            backref='author',
            lazy=True)

    def __repr__(self):
        return self.username or 'unknown user'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def description(self):
        return dictit(self,'id', 'auth0_id','username')

# Association table between unpublished tutorials and tags
unpublished_tutorial_tag = db.Table('unpublished_tutorials_tags', db.Model.metadata,
        db.Column('left_id', db.Integer, db.ForeignKey('unpublished_tutorials.id')),
        db.Column('right_id', db.Integer, db.ForeignKey('tags.id'))
        )

# Association table between published tutorials and tags
published_tutorial_tag = db.Table('published_tutorials_tags', db.Model.metadata,
        db.Column('left_id', db.Integer, db.ForeignKey('published_tutorials.id')),
        db.Column('right_id', db.Integer, db.ForeignKey('tags.id'))
        )

# Unpublished tutorials, separately implemented from published
# tutorials so changes can be acccepted before publishing without
# causing the published tutorial to cease to be displayed
class Unpublished_Tutorial(db.Model):
    __tablename__ = 'unpublished_tutorials'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    under_review = db.Column(db.Boolean, nullable=False)
    title = db.Column(db.String(), nullable=False)
    text = db.Column(db.String(), nullable=False)
    tags = db.relationship('Tag',
        secondary=unpublished_tutorial_tag,
        back_populates='unpublished_tutorials')
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
 
    def delete(self):
        db.session.delete(self)
        db.session.commit()   

    def short(self):
        return dictit(self,'id','author_id','author','title','tags')
       
    def long(self):
        return dictit(self,'id','author_id', 'author','title','tags','text')
     
# Published tutorials
class Published_Tutorial(db.Model):
    __tablename__ = 'published_tutorials'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(), nullable=False)
    text = db.Column(db.String(), nullable=False)
    tags = db.relationship('Tag',
        secondary=published_tutorial_tag,
        back_populates='published_tutorials')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def short(self):
        return dictit(self,'id','author_id','author','title','tags')
       
    def long(self):
        return dictit(self,'id','author_id','author','title','tags','text')

# Tags to be applied to tutorials when submitted
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    unpublished_tutorials = db.relationship(
        'Unpublished_Tutorial',
        secondary=unpublished_tutorial_tag,
        back_populates='tags')
    
    published_tutorials = db.relationship(
        'Published_Tutorial',
        secondary=published_tutorial_tag,
        back_populates='tags')

    def __repr__(self):
        return self.name

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()



