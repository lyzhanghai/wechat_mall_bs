# -*- coding: utf-8 -*-

import json

from odoo import http
from odoo.http import request

from .. import defs
from .error_code import error_code

import logging

_logger = logging.getLogger(__name__)


class NoticeList(http.Controller):
    @http.route('/<string:sub_domain>/notice/list', auth='public', methods=['GET'])
    def get(self, sub_domain, pageSize):
        try:
            user = request.env['res.users'].sudo().search([('sub_domain', '=', sub_domain)])
            if not user:
                return request.make_response(json.dumps({'code': 404, 'msg': error_code[404]}))

            notice_list = request.env['wechat_mall.notice'].search([
                ('create_uid', '=', user.id),
                ('is_show', '=', True)
            ])
            data = []
            for item in notice_list:
                data.append({
                    "id": item.id,
                    "title": item.title,
                    "sort": item.sort,
                    "is_show": item.is_show,
                })

            response = request.make_response(
                headers={
                    "Content-Type": "json"
                },
                data=json.dumps({
                    'code': 0,
                    'msg': 'success',
                    'data': {
                        'totalRow': len(data),
                        'totalPage': 1,
                        'dataList': data
                    }
                })
            )

            return response

        except Exception as e:
            _logger.exception(e)
            return request.make_response(json.dumps({'code': -1, 'msg': error_code[-1], 'data': e.message}))


class NoticeDetail(http.Controller):
    @http.route('/<string:sub_domain>/notice/detail', auth='public', methods=['GET'])
    def get(self, sub_domain, id):
        try:
            user = request.env['res.users'].sudo().search([('sub_domain', '=', sub_domain)])
            if not user:
                return request.make_response(json.dumps({'code': 404, 'msg': error_code[404]}))

            notice = request.env['wechat_mall.notice'].search([
                ('id', '=', id)
            ])
            response = request.make_response(
                headers={
                    "Content-Type": "json"
                },
                data=json.dumps({
                    'code': 0,
                    'msg': 'success',
                    'data': {
                        'content': notice.content,
                        'dateAdd': notice.create_date,
                        'id': notice.id,
                        'isShow': notice.is_show,
                        'title': notice.title,
                        'userId': user.id
                    }
                })
            )

            return response

        except Exception as e:
            _logger.exception(e)
            return request.make_response(json.dumps({'code': -1, 'msg': error_code[-1], 'data': e.message}))
