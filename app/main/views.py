# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 视图层
'''

from flask import render_template
from . import main_bp
from flask_login import login_required


@main_bp.route('/', methods=['GET','POST'])
@login_required
def index():
    # form = NameForm()
    # if form.validate_on_submit():
    #     return redirect(url_for('main.index'))
    return render_template('main/index.html', title_name='Index')


