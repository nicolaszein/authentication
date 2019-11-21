from flask import Blueprint, render_template

app = Blueprint(
    'auth_app', __name__,
    url_prefix='/auth',
    template_folder='templates',
    static_folder='static'
)


@app.route('/activate')
def activate():
    return render_template('activate.html')
