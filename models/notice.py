# -*- coding: utf-8 -*-

from odoo import models, fields, api

from .. import defs


class Notice(models.Model):
    _name = 'wechat_mall.notice'
    _description = u'通知'
    _rec_name = 'title'
    _order = 'sort'

    title = fields.Char(string='名称', required=True)
    sort = fields.Integer(string='排序')
    is_show = fields.Boolean(string='是否显示', default=True)
    content = fields.Html(string='内容')
