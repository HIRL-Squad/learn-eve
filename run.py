from app.apiserver import ApiServer

app = ApiServer()
app.configure()

if __name__ == '__main__':
    app.run()