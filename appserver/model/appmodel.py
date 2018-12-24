from app import db
from datetime import date

class Userinfo(db.Model):

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(20),nullable=False,unique=True)
    passwd = db.Column(db.String(20),nullable=False)
    type =db.Column(db.Integer,nullable=False)
    usertime=db.Column(db.Date,nullable=False,default=date.today())

    def __repr__(self):
        return '<User %r>' % self.name

    def jsonstr(self):
        jsonstr = {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'usertime': self.usertime.strftime("%Y-%m-%d"),
            'aaa':"bbbbbb"
        }
        return jsonstr



artist_songs = db.Table('artist_songs',
      db.Column('song_id', db.Integer, db.ForeignKey('songs.id')),
      db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'))
)


class songs(db.Model):

    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=True)
    lyrics = db.Column(db.Text(), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    artists = db.relationship('artists', secondary=artist_songs, backref=db.backref('artists'), lazy="select")
    lyric_copies = db.relationship('lyric_copies', backref='songs', lazy='select')

    def jsonstr(self):
        artist = []
        if self.artists is not None and len(self.artists) != 0:
            for art in self.artists:
                artist.append(art.name)

        lyricarr = []
        if self.lyric_copies is not None and len(self.lyric_copies) != 0:
            for lyr in self.lyric_copies:
                lyricarr.append(lyr.jsonstr())

        jsondata = {
            'ID': self.id,
            'title': self.title,
            'artist': artist,
            'lyric': self.lyrics,
            'copyrights': {
                'lyric': lyricarr
            }
        }
        return jsondata


class artists(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=True)
    gender = db.Column(db.Integer, nullable=True)
    location = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)


class lyric_copies(db.Model):
    __tablename__ = 'lyric_copies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=True)
    end_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)

    def jsonstr(self):
        enddatestr = ''
        if self.end_date is not None and self.end_date != '':
            enddatestr = self.end_date.strftime('%Y-%m-%d')
        else:
            enddatestr = '永久'

        jsonstr = {
            "lyricists": self.name,
            "endDate": enddatestr
        }
        return jsonstr



