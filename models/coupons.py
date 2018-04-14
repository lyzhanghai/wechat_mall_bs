# -*- coding: utf-8 -*-

from odoo import models, fields, api

from .. import defs


class Coupons(models.Model):
    _name = 'wechat_mall.coupons'
    _description = u'优惠券'
    _rec_name = 'name'
    _order = 'moneyMax'

    name = fields.Char(string='名称')
    dateEndType = fields.Selection(defs.CouponsDateEndType.attrs.items(), string='过期方式',
                                   default=defs.CouponsDateEndType.valid_days)
    dateEndDays = fields.Integer(string='有效天数')
    dateEnd = fields.Datetime(string='截止时间')
    moneyHreshold = fields.Float(string='最低消费')
    moneyMax = fields.Float(string='优惠券额度')
    numberPersonMax = fields.Integer(string='最大拥有数', default=1)
    numberLeft = fields.Integer(string='剩余个数')
    numberTotle = fields.Integer(string='总个数')
    numberUsed = fields.Integer(string='已使用个数', default=0)