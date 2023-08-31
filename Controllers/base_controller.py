from flask import request
from flask_restful import Resource

from Responses.Response import JSONResponse


class BaseController(Resource):
    DEFAULT_PER_PAGE = 10
    DEFAULT_PAGE = 1
    response = JSONResponse()

    def get_current_page(self):
        return request.args.get('page', self.DEFAULT_PAGE, type=int)

    def get_per_page(self):
        return request.args.get('per_page', self.DEFAULT_PER_PAGE, type=int)
