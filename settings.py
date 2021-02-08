from app.auth.token import JwtAuth

MARKER_API_URL = 'http://127.0.0.1:5001/'

MONGO_USERNAME = 'chi'
MONGO_PASSWORD = 'D@feige666'
MONGO_DBNAME = 'eve'

# Eve Global Config Overrides
DATE_FORMAT = "%d/%m/%Y %H:%M:%S"
DATE_CREATED = "created_at"
LAST_UPDATED = "updated_at"
PAGINATION = False # turn off pagination
IF_MATCH = False

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

schema = {
    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/pyeve/cerberus) for details.
    'firstname': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 10,
    },
    'lastname': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 15,
        'required': True,
        # talk about hard constraints! For the purpose of the demo
        # 'lastname' is an API entry-point, so we need it to be unique.
        'unique': True,
    },
    # 'role' is a list, and can only contain values from 'allowed'.
    'role': {
        'type': 'list',
        'allowed': ["author", "contributor", "copy"],
    },
    # An embedded 'strongly-typed' dictionary.
    'location': {
        'type': 'dict',
        'schema': {
            'address': {'type': 'string'},
            'city': {'type': 'string'}
        },
    },
    'born': {
        'type': 'datetime',
    },
}

people = {
    # 'title' tag used in item links. Defaults to the resource title minus
    # the final, plural 's' (works fine in most cases but not for 'people')
    'item_title': 'person',

    # by default the standard item entry point is defined as
    # '/people/<ObjectId>'. We leave it untouched, and we also enable an
    # additional read-only entry point. This way consumers can also perform
    # GET requests at '/people/<lastname>'.
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'lastname'
    },

    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST'],

    'schema': schema
}

patient_schema = {
    'patient_id': {
        'type': 'string',
        'unique': True
    },
    'visit': {
        'type': 'string',
        'allowed': ['baseline', 'six_months']
    },
    'current_medications': {
        'type': 'string',
    },
    'occupation': {
        'type': 'string',
    },
    'living_arrangements': {
        'type': 'string',
    },
    'housing_type': {
        'type': 'string',
    },
    'charleston_scale': {
        'type': 'list'
    },
    'high_blood_pressure': {
        'type': 'list',
    },
    'high_cholesterol': {
        'type': 'number',
    },
    'diabetes_mellitus': {
        'type': 'number',
    },
    'setting_of_assessment': {
        'type': 'string',
        'allowed': ['test', 'trial']
    },
    'level_of_education':{
        'type': 'string'
    },
    'assessment_date': {
        'type': 'datetime'
    },
    'assessment_date_calendar': {
        'type': 'integer'
    },
    "date_of_birth": {
        'type': 'datetime'
    },
    "date_of_birth_calendar": {
        'type': 'integer'
    },
    'gender': {
        'type': 'string',
        'allowed': ['Male', 'Female', 'male', 'female']
    },
    'ethnicity': {
        'type': 'string',
        'allowed': ['Chinese', 'Malay', 'Indian', 'Others', 'chinese', 'malay', 'indian', 'others']
    },
    'dominant_hand': {
        'type': 'string',
        'allowed': ['left', 'right', 'both']
    },
    'annual_income':{
        'type': 'string'
    },
    'option_of_money':{
        'type': 'string'
    },
    'note':{
        'type': 'string'
    },
    'sarc_f': {
        'type': 'list'
    },
    'site': {
        'type':'string'
    },
    'mmse_score': {
        'type': 'number',
    },
    'moca_score': {
        'type': 'number',
    },
    'diagnosis': {
        'type': 'string'
    }
}

patient = {
    'item_title': 'patient',
    'item_url': 'regex("[a-zA-Z0-9]{1,10}")',
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH'],
    # 'authentication': JwtAuth,
    'schema': patient_schema
}

test_result_schema = {
    'name': {'type': 'string',
             'unique': True},
    'score': {'type': 'string'},
    'pic': {'type': 'media'}
}

test_data_schema = {
    'test': {
        'type': 'dict'
    },
    'human_correction': {
        'type': 'dict'
    },
    'patient_id':{
        'type': 'objectid',
        'data_relation': {
            'resource': 'patient',
            'field': '_id',
            'embeddable': True
        }
    },
    'patient_name':{
        'type': 'string'
    },
    'device_info': {
        'type': 'dict',
        'nullable': True
    }
}


test_result = {
    'resource_methods': ['GET'],
    'datasource': {
        'source': 'testdata',
        'projection': {'_id': 1,
                       'patient_id': 1,
                       'patient_name': 1,
                       'result': 1}
    }
}

test_data = {
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH'],
    'schema': test_data_schema
}


test_list = {
    'allowed_filters': ['*'],
    'datasource': {
        'source': 'testdata',
        'projection': {'_id': 1,
                       'patient_id': 1,
                       'patient_name': 1}
    }
}


DOMAIN = {'people': people,
          'patient': patient,
          'testdata': test_data,
          'testresult': test_result,
          'testlist': test_list}
