# Package: dmcb
# abort(http code) and sendfile(file) function
from flask import abort, send_file;
# The Flask app and cache and the generator
from dmcb import app, cache, generator;

# The views:

#@app.cache.cached(timeout=app.config['TIMEOUT'])
@app.route('/<name>/<adress>/banner.png')
def name_adress(name, adress):
    return send_file(generator.banner(name, adress), mimetype="image/png", as_attachment=False)

#@cache.cached(timeout=app.config['TIMEOUT'])
@app.route('/<name>/<adress>/<int:port>/banner.png')
def name_adress_port(name, adress, port):
    return send_file(generator.banner(name, adress, port=port), mimetype="image/png", as_attachment=False)

#@cache.cached(timeout=app.config['TIMEOUT'])
@app.route('/<version>/<name>/<adress>/banner.png')
def version_name_adress(version, name, adress):
    if not (version == '1.7' or version == '1.6'):
        abort(404)
        return
    return send_file(generator.banner(name, adress, version=version), mimetype="image/png", as_attachment=False)

#@cache.cached(timeout=app.config['TIMEOUT'])
@app.route('/<version>/<name>/<adress>/<int:port>/banner.png')
def version_name_adress_port(version, name, adress, port):
    if not (version == '1.7' or version == '1.6'):
        abort(404)
        return
    return send_file(generator.banner(name, adress, port=port, version=version), mimetype="image/png", as_attachment=False)
    