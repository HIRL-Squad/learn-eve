from eve import Eve

from app import app


def on_inserted_testdata_callback(items):
    for item in items:
        test = item['test']
    print("pre-request callback!")


class ApiServer(Eve):
    def configure(self):
        self.on_inserted_testdata += on_inserted_testdata_callback


@app.route('/data_migration')
def data_migration():
    pass
