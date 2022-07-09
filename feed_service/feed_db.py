from feed_service import feed_db as database


class Online(database.Model):
    __tablename__ = 'online'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    uid = database.Column(database.Integer(), unique=True)

    def __init__(self, uid):
        self.uid = uid


class Feed(database.Model):
    __tablename__ = 'feed'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    uid = database.Column(database.Integer())
    post_id = database.Column(database.Integer())
    date = database.Column(database.DateTime())

    def __init__(self, uid, post_id, date):
        self.uid = uid
        self.post_id = post_id
        self.date = date
