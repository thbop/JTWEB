import jtweb

app = jtweb.app()

@app.page('/')
def test():
    return 'Thbop returns'

@app.page('/bobbyj')
def test():
    return 'Bobby J returns'

if __name__ == '__main__':
    app.run()