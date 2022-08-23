from flask_rest_paginate import Pagination
from flask_sqlalchemy import Pagination as SqlalchemyPaginationObject

pagination = Pagination()


def paginate_hook(current_page: int, page_obj: SqlalchemyPaginationObject) -> dict:
    return {
        "current_page": current_page,
        "per_page": page_obj.per_page,
        "pages": page_obj.pages,
    }
