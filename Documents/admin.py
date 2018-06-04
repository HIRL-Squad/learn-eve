from app.admin.base import AuthModelView



def get_test_score(view, context, model, name):
    score = 0
    max_score = 0
    if model.result:
        max_score = len(model.result.values())
        for correctness in model.result.values():
            if correctness:
                score += 1
    return str(score) + '/' + str(max_score)


class PatientView(AuthModelView):
    pass


class TestdataView(AuthModelView):
    list_template = 'admin/model/testdata_list.html'
    column_default_sort = ('updated_at', True)
    column_filters = ('patient_id', 'patient_name')
    column_formatters = dict(result=get_test_score)
    column_exclude_list = ['test']

    def render(self, template, **kwargs):
        kwargs['get_score_link'] = self.get_score_link
        return super(TestdataView, self).render(template, **kwargs)

    def get_score_link(self, row):
        return "../../testimage/"+str(row.id)
