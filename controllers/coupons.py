# -*- coding: utf-8 -*-

import json

from odoo import http, fields
from odoo.http import request

from .. import defs
from .error_code import error_code

import logging

_logger = logging.getLogger(__name__)


class CouponsList(http.Controller):
    @http.route('/<string:sub_domain>/discounts/coupons', auth='public', methods=['GET'])
    def get(self, sub_domain, type):
        try:
            user = request.env['res.users'].sudo().search([('sub_domain', '=', sub_domain)])
            if not user:
                return request.make_response(json.dumps({'code': 404, 'msg': error_code[404]}))

            search_params = [('create_uid', '=', user.id)]
            if type:
                search_params.append(('dateEndType', "=", type))
            coupons_list = request.env(user=user.id)['wechat_mall.coupons'].search(search_params)
            data = []
            for item in coupons_list:
                data.append({
                    "id": item.id,
                    "dateAdd": item.create_date,
                    "dateEndType": item.dateEndType,
                    "dateEndDays": item.dateEndDays,
                    "dateEnd": item.dateEnd,
                    "moneyHreshold": item.moneyHreshold,
                    "moneyMax": item.moneyMax,
                })

            response = request.make_response(
                headers={
                    "Content-Type": "json"
                },
                data=json.dumps({
                    'code': 0,
                    'msg': 'success',
                    'data': data
                })
            )

            return response

        except Exception as e:
            _logger.exception(e)
            return request.make_response(json.dumps({'code': -1, 'msg': error_code[-1], 'data': e.message}))


class CouponsFetch(http.Controller):
    @http.route('/<string:sub_domain>/discounts/fetch', auth='public', methods=['GET'])
    def get(self, sub_domain, coupons_id, token=None):
        try:
            user = request.env['res.users'].sudo().search([('sub_domain', '=', sub_domain)])
            if not user:
                return request.make_response(json.dumps({'code': 404, 'msg': error_code[404]}))

            if not token:
                return request.make_response(json.dumps({'code': 300, 'msg': error_code[300].format('token')}))

            access_token = request.env(user=user.id)['wechat_mall.access_token'].search([
                ('token', '=', token),
                ('create_uid', '=', user.id)
            ])

            if not access_token:
                return request.make_response(json.dumps({'code': 901, 'msg': error_code[901]}))

            wechat_user = request.env(user=user.id)['wechat_mall.user'].search([
                ('open_id', '=', access_token.open_id),
                ('create_uid', '=', user.id)
            ])
            if not wechat_user:
                return request.make_response(json.dumps({'code': 10000, 'msg': error_code[10000]}))

            # 是否有剩余
            coupons = request.env(user=user.id)['wechat_mall.coupons'].search([
                ('create_uid', '=', user.id),
                ('id', '=', coupons_id)
            ])
            if not coupons:
                response = request.make_response(
                    headers={
                        "Content-Type": "json"
                    },
                    data=json.dumps({
                        'code': 20001,
                        'msg': 'failed',
                    })
                )
                return response

            # 是否已过期
            if coupons.dateEndType == 'deadline' and coupons.dateEnd > fields.datetime.now():
                response = request.make_response(
                    headers={
                        "Content-Type": "json"
                    },
                    data=json.dumps({
                        'code': 20004,
                        'msg': 'failed',
                    })
                )
                return response

            # 是否已领过
            user_coupons = request.env(user=user.id)['wechat_mall.user.coupons'].search([
                ('create_uid', '=', user.id),
                ('coupons_id', '=', coupons_id)
            ])
            if user_coupons:
                if user_coupons.number > coupons.numberPersonMax:
                    response = request.make_response(
                        headers={
                            "Content-Type": "json"
                        },
                        data=json.dumps({
                            'code': 20003,
                            'msg': 'failed',
                        })
                    )
                    return response
                else:
                    # 领成功了
                    user_coupons.write({
                        'number': user_coupons.number + 1
                    })
            else:
                # 领成功了
                request.env(user=user.id)['wechat_mall.user.coupons'].create({
                    "user_id": wechat_user.id,
                    "coupons_id": coupons.id,
                    "name": coupons.name,
                    "dateEndType": coupons.dateEndType,
                    "dateEndDays": coupons.dateEndDays,
                    "dateEnd": coupons.dateEnd,
                    "moneyHreshold": coupons.moneyHreshold,
                    "moneyMax": coupons.moneyMax,
                    "number": 1,
                })
            response = request.make_response(
                headers={
                    "Content-Type": "json"
                },
                data=json.dumps({
                    'code': 0,
                    'msg': 'success',
                })
            )

            return response

        except Exception as e:
            _logger.exception(e)
            return request.make_response(json.dumps({'code': -1, 'msg': error_code[-1], 'data': e.message}))


class MyCoupons(http.Controller):
    @http.route('/<string:sub_domain>/discounts/my', auth='public', methods=['GET'])
    def get(self, sub_domain, status, token=None):
        try:
            user = request.env['res.users'].sudo().search([('sub_domain', '=', sub_domain)])
            if not user:
                return request.make_response(json.dumps({'code': 404, 'msg': error_code[404]}))

            if not token:
                return request.make_response(json.dumps({'code': 300, 'msg': error_code[300].format('token')}))

            access_token = request.env(user=user.id)['wechat_mall.access_token'].search([
                ('token', '=', token),
                ('create_uid', '=', user.id)
            ])

            if not access_token:
                return request.make_response(json.dumps({'code': 901, 'msg': error_code[901]}))

            wechat_user = request.env(user=user.id)['wechat_mall.user'].search([
                ('open_id', '=', access_token.open_id),
                ('create_uid', '=', user.id)
            ])
            if not wechat_user:
                return request.make_response(json.dumps({'code': 10000, 'msg': error_code[10000]}))

            user_coupons_list = request.env(user=user.id)['wechat_mall.user.coupons'].search([
                ('create_uid', '=', user.id),
            ])
            data = []
            for item in user_coupons_list:
                data.append({
                    "id": item.id,
                    "user_id": wechat_user.id,
                    "coupons_id": item.coupons_id,
                    "name": item.name,
                    "dateEndType": item.dateEndType,
                    "dateEndDays": item.dateEndDays,
                    "dateEnd": item.dateEnd,
                    "moneyHreshold": item.moneyHreshold,
                    "money": item.moneyMax,
                    "number": item.number,
                })

            response = request.make_response(
                headers={
                    "Content-Type": "json"
                },
                data=json.dumps({
                    'code': 0,
                    'msg': 'success',
                    'data': data,
                })
            )

            return response

        except AttributeError:
            return request.make_response(json.dumps({'code': 404, 'msg': error_code[404]}))

        except Exception as e:
            _logger.exception(e)
            return request.make_response(json.dumps({'code': -1, 'msg': error_code[-1], 'data': e.message}))