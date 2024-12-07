from typing import Any

from beanie import Document, PydanticObjectId
from pydantic import BaseModel

class Database:
    def __init__(self, model):
        self.model = model

    @staticmethod
    async def create(document: Document) -> None:
        await document.create()
        return

    async def get(self, doc_id: PydanticObjectId) -> Any:
        doc = await self.model.get(doc_id)
        if doc:
            return doc

    async def get_all(self) -> list[Any]:
        docs = await self.model.find_all().to_list()
        return docs

    async def update(self, doc_id: PydanticObjectId, document: BaseModel) -> Any:
        update_query = {"$set": {k: v for k, v in document.model_dump().items() if v is not None}}

        doc = await self.get(doc_id)
        if not doc:
            return False

        await doc.update(update_query)
        return doc

    async def delete(self, doc_id: PydanticObjectId) -> bool:
        doc = await self.get(doc_id)
        if not doc:
            return False

        await doc.delete()
        return True
