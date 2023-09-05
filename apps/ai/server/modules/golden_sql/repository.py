from bson.objectid import ObjectId

from config import GOLDEN_SQL_COL, GOLDEN_SQL_REF_COL, QUERY_RESPONSE_REF_COL
from database.mongo import DESCENDING, MongoDB
from modules.golden_sql.models.entities import GoldenSQL, GoldenSQLRef
from utils.misc import get_next_display_id, get_object_id


class GoldenSQLRepository:
    def get_golden_sql(self, object_id: ObjectId) -> GoldenSQL:
        golden_sql = MongoDB.find_by_object_id(GOLDEN_SQL_COL, get_object_id(object_id))
        return GoldenSQL(**golden_sql) if golden_sql else None

    def get_golden_sqls(self, object_ids: list[ObjectId]) -> list[GoldenSQL]:
        golden_sqls = MongoDB.find_by_object_ids(GOLDEN_SQL_COL, object_ids)
        return [GoldenSQL(**gs) for gs in golden_sqls]

    def get_golden_sql_ref(self, object_id: ObjectId) -> GoldenSQLRef:
        golden_sql_ref = MongoDB.find_one(
            GOLDEN_SQL_REF_COL, {"golden_sql_id": get_object_id(object_id)}
        )
        return GoldenSQLRef(**golden_sql_ref) if golden_sql_ref else None

    def get_golden_sql_refs(
        self, skip: int, limit: int, order: str, org_id: ObjectId
    ) -> list[GoldenSQLRef]:
        golden_sql_refs = (
            MongoDB.find(GOLDEN_SQL_REF_COL, {"organization_id": org_id})
            .sort([(order, DESCENDING)])
            .skip(skip)
            .limit(limit)
        )
        return [GoldenSQLRef(**gsr) for gsr in golden_sql_refs]

    def get_verified_golden_sql_ref(self, query_response_id: ObjectId) -> GoldenSQLRef:
        golden_sql_ref = MongoDB.find_one(
            GOLDEN_SQL_REF_COL, {"query_response_id": query_response_id}
        )
        return GoldenSQLRef(**golden_sql_ref) if golden_sql_ref else None

    def add_golden_sql_ref(
        self,
        golden_sql_ref_data: dict,
    ) -> str:
        return str(
            MongoDB.insert_one(GOLDEN_SQL_REF_COL, golden_sql_ref_data),
        )

    def delete_golden_sql_ref(self, golden_sql_id: ObjectId) -> int:
        return MongoDB.delete_one(GOLDEN_SQL_REF_COL, {"golden_sql_id": golden_sql_id})

    def delete_verified_golden_sql_ref(self, query_response_id: ObjectId):
        return MongoDB.delete_one(
            GOLDEN_SQL_REF_COL, {"query_response_id": query_response_id}
        )

    def get_next_display_id(self, org_id: ObjectId) -> str:
        return get_next_display_id(GOLDEN_SQL_REF_COL, org_id, "GS")

    def get_verified_query_display_id(self, query_response_id: ObjectId) -> str:
        query_ref = MongoDB.find_one(
            QUERY_RESPONSE_REF_COL, {"query_response_id": query_response_id}
        )

        if not query_ref:
            return None

        if "display_id" not in query_ref:
            return "QR-00000"

        return query_ref["display_id"]