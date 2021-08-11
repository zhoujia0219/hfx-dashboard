from flask import Blueprint
from flask import redirect

from conf.router_conts import URL_SALES_BYMONTH

blueprint = Blueprint(
    'base_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)


@blueprint.route('/')
def index():
    return redirect(URL_SALES_BYMONTH)
