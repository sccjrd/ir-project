# crawler/scraper/build_hacks_all.py

import os
from typing import List

from pymongo import MongoClient
from dotenv import load_dotenv

# Load env vars from .env in this folder (MONGO_URI, MONGO_DB_NAME)
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "ikea_hacks_ir")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not set in .env")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]


def get_source_collections() -> List[str]:
    """
    Return all collections that start with 'hacks_' except 'hacks_all'.
    """
    names = db.list_collection_names()
    return [
        name
        for name in names
        if name.startswith("hacks_") and name != "hacks_all"
    ]


def build_hacks_all(drop_existing: bool = True):
    """
    Build (or rebuild) the hacks_all collection by merging all hacks_* collections.
    Uses (url, source) as a natural key to avoid duplicates.
    """
    target = db["hacks_all"]

    if drop_existing:
        print("Dropping existing hacks_all collection...")
        target.drop()

    source_collections = get_source_collections()
    print(f"Source collections: {source_collections}")

    total_inserted = 0

    for coll_name in source_collections:
        coll = db[coll_name]
        # Derive a source name from the collection name (e.g. hacks_ikea -> ikea)
        source_name = coll_name[len("hacks_"):]

        count = coll.count_documents({})
        print(f"Processing {coll_name} (source='{source_name}', {count} docs)")

        cursor = coll.find({})
        for doc in cursor:
            # Remove Mongo's internal _id; we don't reuse it.
            doc.pop("_id", None)

            # Ensure 'source' field is set
            if not doc.get("source"):
                doc["source"] = source_name

            url = doc.get("url")
            if not url:
                # If there's no URL, we skip; it's a broken document for our use case.
                continue

            # Natural key: (url, source)
            key = {"url": url, "source": doc["source"]}

            # Upsert into hacks_all
            result = target.update_one(key, {"$set": doc}, upsert=True)
            if result.upserted_id is not None:
                total_inserted += 1

    print(f"Done. Total new docs inserted into hacks_all: {total_inserted}")
    print(
        f"hacks_all now has {db['hacks_all'].count_documents({})} documents.")


if __name__ == "__main__":
    build_hacks_all(drop_existing=True)
