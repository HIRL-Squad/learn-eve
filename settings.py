from app.auth.token import JwtAuth

MARKER_API_URL = 'http://127.0.0.1:5001/'

# Eve Global Config Overrides
DATE_FORMAT = "%d/%m/%Y %H:%M:%S"
DATE_CREATED = "created_at"
LAST_UPDATED = "updated_at"
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
    'patient_name': {
        'type': 'string',
    },
    'dominant_hand': {
        'type': 'string',
        'allowed': ['left', 'right', 'both']
    },
    'date_of_birth': {
        'type': 'datetime'
    },
    'assessment_date': {
        'type': 'datetime'
    },
    'nihss':{
        'type': 'integer'
    },
    'mrs':{
        'type': 'integer'
    },
    'years_of_education':{
        'type': 'integer'
    },
    'ethnicity': {
        'type': 'string',
        'allowed': ['Chinese','Malay','Indian', 'Others']
    },
    'gender': {
        'type': 'string',
        'allowed': ['Male', 'Female']
    },
    'onset_of_stroke': {
        'type': 'datetime'
    },
    'setting_of_assessment':{
        'type': 'string',
        'allowed': ['ward', 'clinic', 'community']
    }
}

patient = {
    'item_title': 'patient',
    'item_url': 'regex("[\d]{3,4}")',
    'resource_methods': ['GET', 'POST'],
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
