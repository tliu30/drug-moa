import web
from web import form

urls = (
    '/', 'index',
    '/view', 'view',
    '/upload', 'upload'
)

render = web.template.render('templates/', base='layout')

upload_form = form.Form( 
    form.File("myfile"))

class index:
    def GET(self):
        return render.index()

class view:
    def GET(self):
        return render.view()

class upload:
    def GET(self):
        form = upload_form()
        return render.upload(form)

    def POST(self):
        x = web.input(myfile={})
        filedir = 'tmp'
        if 'myfile' in x:
            fname = x.myfile.filename.split('/')[-1]
            fout = open(filedir + '/' + fname, 'wb')
            fout.write(x.myfile.file.read())
            fout.close()
        raise web.seeother('/upload')  

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
