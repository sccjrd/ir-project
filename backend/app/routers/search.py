from fastapi import APIRouter, Depends, Query, HTTPException
from bson import ObjectId
from typing import List
import math

from app.models import Hack, SearchResult
from app.services import mongo
from app.utils import mongo_doc_to_hack  

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("/", response_model=SearchResult)
def search_hacks(
    query: str = Query(..., description="Search term"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db = Depends(mongo.get_db),
):
    """
    Search API to query the hacks_all collection using MongoDB Atlas Search.
    - Uses $search for ranked hits
    - Uses $searchMeta for true total count
    """
    index_name = mongo.MONGO_SEARCH_INDEX
    collection = db["hacks_all"]

    # ---------- 1) $search for the current page of hits ----------
    skip = (page - 1) * page_size

    search_pipeline = [
        {
        "$search": {
            "index": index_name,
            "compound": {
            "must": [
                {
                "text": {
                    "query": query,
                    "path": ["title", "content"],
                    # "fuzzy": {"maxEdits": 1}  # optional
                }
                }
            ],
            "should": [
                { "text": { "query": query, "path": ["categories", "tags"] } }
            ]
            }
        }
        },
        {
            "$project": {
                "_id": 0,
                "id": {"$toString": "$_id"},
                "source": 1,
                "url": 1,
                "author": 1,
                "categories": 1,
                "content": 1,
                "date": 1,
                "excerpt": 1,
                "image_url": 1,
                "tags": 1,
                "title": 1,
                "score": {"$meta": "searchScore"},
            }
        },
        {"$skip": skip},
        {"$limit": page_size},
    ]

    hit_docs = list(collection.aggregate(search_pipeline))
    hits: List[Hack] = [Hack(**doc) for doc in hit_docs]

    # ---------- 2) $searchMeta to get true total matches ----------
    count_pipeline = [
        {
            "$searchMeta": {
                "index": index_name,
                "compound": {
                "must": [
                    {
                    "text": {
                        "query": query,
                        "path": ["title", "content"],
                        # "fuzzy": {"maxEdits": 1}  # optional
                    }
                    }
                ],
                "should": [
                    { "text": { "query": query, "path": ["categories", "tags"] } }
                ]
                },
                "count": {
                    "type": "total",
                },
            }
        }
    ]

    meta_docs = list(collection.aggregate(count_pipeline))
    if meta_docs and "count" in meta_docs[0]:
        total = meta_docs[0]["count"]["total"]
    else:
        total = 0

    total_pages = math.ceil(total / page_size) if total > 0 else 0

    return SearchResult(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        hits=hits,
    )


@router.get("/similar/{hack_id}", response_model=List[Hack])
def get_similar_hacks(
    hack_id: str,
    limit: int = Query(6, ge=1, le=20),
    db = Depends(mongo.get_db),
):
    collection = db["hacks_all"]
    index_name = mongo.MONGO_SEARCH_INDEX

    # ---------- 1) Validate and fetch the reference document ---------
    try:
        obj_id = ObjectId(hack_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid hack_id")

    ref_doc = collection.find_one({"_id": obj_id})
    if not ref_doc:
        raise HTTPException(status_code=404, detail="Hack not found")

    # -------- 2) moreLikeThis search on title/content/categories/tags -----
    pipeline = [
        {
            "$search": {
                "index": index_name,
                "moreLikeThis": {
                    "like": [
                        {
                            "title": ref_doc.get("title", ""),
                            "content": ref_doc.get("content", ""),
                            "categories": ref_doc.get("categories", []),
                            "tags": ref_doc.get("tags", []),
                        }
                    ],
                },
            }
        },
        {"$match": {"_id": {"$ne": obj_id}}},
        {
            "$project": {
                "_id": 1,
                "source": 1,
                "title": 1,
                "content": 1,
                "author": 1,
                "date": 1,
                "url": 1,
                "categories": 1,
                "tags": 1,
                "image_url": 1,
                "excerpt": 1,
                "score": {"$meta": "searchScore"},
            }
        },
        {"$limit": limit},
    ]

    docs = list(collection.aggregate(pipeline))
    return [mongo_doc_to_hack(doc) for doc in docs]

