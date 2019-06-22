import os
from app import create_app, db
from app.models import User, Role
from flask_migrate import Migrate


app = create_app(os.getenv('FLASK_CONFIG') or 'development')
migrate = Migrate(app, db)

# set FLASK_APP=jobbole.py
# set FALSK_DEBUG=1
# flask run

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

# topbar = Navbar(u'Flask入门',
#                     View('Home', 'main.index'),
#                     View('Your Account', 'main.index'),
#                 Subgroup(u'项目',
#                          View(u'项目一', 'main.index'),
#                          Separator(),
#                          View(u'项目二', 'main.index'),
#                          ),
#                     )
#
# nav = Nav()
# nav.register_element('top', topbar)
# nav.init_app(app)


if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # debug模式启动，重载器与调试器