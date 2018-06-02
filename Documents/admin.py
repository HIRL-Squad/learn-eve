from app.admin.base import AuthModelView


class PatientView(AuthModelView):
    pass


class TestdataView(AuthModelView):
    list_template = 'admin/model/testdata_list.html'

    def render(self, template, **kwargs):
        kwargs['get_score_link'] = self.get_score_link
        kwargs['get_score'] = self.get_score
        return super(TestdataView, self).render(template, **kwargs)

    def get_score_link(self, row):
        return "../../testimage/"+str(row.id)

    def get_score(self, row):
        score = 0
        max_score = len(row.test['vas_cog_block'])
        if row.test.get('result'):
            max_score = len(row.test['result'].values())
            for correctness in row.test['result'].values():
                if correctness:
                    score += 1
        return str(score)+'/'+str(max_score)
