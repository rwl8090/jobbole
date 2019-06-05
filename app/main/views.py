# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 视图层
'''

from flask import render_template, session, redirect, url_for
from . import main_bp



@main_bp.route('/', methods=['GET','POST'])
def index():


    # form = NameForm()
    # if form.validate_on_submit():
    #     return redirect(url_for('main.index'))
    return render_template('index.html', title_name='Index')
