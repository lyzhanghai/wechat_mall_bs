# -*- coding: utf-8 -*-

from odoo import models, fields, api

from .. import defs


class WechatUser(models.Model):
    _name = 'wechat_mall.user'
    _description = u'微信用户'

    name = fields.Char('昵称')
    open_id = fields.Char('OpenId', required=True, index=True)
    union_id = fields.Char('UnionId')
    gender = fields.Integer('gender')
    language = fields.Char('语言')
    register_type = fields.Selection(defs.WechatUserRegisterType.attrs.items(), string='注册来源',
                                     default=defs.WechatUserRegisterType.app)
    phone = fields.Char('手机号码')
    country = fields.Char('国家')
    province = fields.Char('省份')
    city = fields.Char('城市')
    avatar = fields.Html('头像', compute='_compute_avatar')
    avatar_url = fields.Char('头像链接')
    register_ip = fields.Char('注册IP')
    last_login = fields.Datetime('登陆时间')
    ip = fields.Char('登陆IP')
    status = fields.Selection(defs.WechatUserStatus.attrs.items(), string='状态',
                              default=defs.WechatUserStatus.default)

    address_ids = fields.One2many('wechat_mall.address', 'wechat_user_id', string='收货地址')
    order_ids = fields.One2many('wechat_mall.order', 'wechat_user_id', string='订单')
    coupons_ids = fields.One2many('wechat_mall.coupons', 'id', string='优惠券')

    balance = fields.Float('可用余额', default=0)
    freeze = fields.Float('冻结金额', default=0)
    score = fields.Integer('积分', default=0)


    _sql_constraints = [(
        'wechat_mall_user_union_id_unique',
        'UNIQUE (union_id, create_uid)',
        'wechat user open_id with create_uid is existed！'
    ),
        (
            'wechat_mall_user_open_id_unique',
            'UNIQUE (open_id, create_uid)',
            'wechat user open_id with create_uid is existed！'
        ),
    ]

    @api.multi
    @api.depends('avatar_url')
    def _compute_avatar(self):
        for each_record in self:
            if each_record.avatar_url:
                each_record.avatar = """
                <img src="{avatar_url}" style="max-width:100px;">
                """.format(avatar_url=each_record.avatar_url)
            else:
                each_record.avatar = False


class UserCoupons(models.Model):
    _name = 'wechat_mall.user.coupons'
    _description = u'用户优惠券'

    user_id = fields.Many2one('wechat_mall.user', string='用户', required=True, ondelete='cascade')

    # 冗余记录商品，防止商品删除后订单数据不完整
    coupons_id = fields.Integer('优惠券id')
    name = fields.Char(string='名称')
    dateEndType = fields.Selection(defs.CouponsDateEndType.attrs.items(), string='过期方式',
                                   default=defs.CouponsDateEndType.valid_days)
    dateEndDays = fields.Integer(string='有效天数')
    dateEnd = fields.Datetime(string='截止时间')
    moneyHreshold = fields.Float(string='最低消费')
    moneyMax = fields.Float(string='优惠券额度')
    number = fields.Integer(string='当前个数')