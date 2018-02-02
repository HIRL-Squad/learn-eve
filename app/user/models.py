from mongoengine import Document, StringField, ListField, ReferenceField


class Role(Document):
    name = StringField(required=True, max_length=80, unique=True)
    description = StringField(max_length=255)

    def __str__(self):
        return self.name


class User(Document):
    username = StringField(primary_key=True)
    password = StringField()
    display_name = StringField()
    roles = ListField(ReferenceField(Role),default=[])

    def __init__(self, email, password, display_name, *args, **values):
        super().__init__(*args, **values)
        self.username = email
        self.password = password
        self.display_name = display_name

    def __init__(self, *args, **values):
        super().__init__(*args, **values)

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.username)