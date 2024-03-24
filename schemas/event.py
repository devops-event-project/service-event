from datetime import datetime

"""
Provides serialization functions to facilitate the data exchange between the 
API service and MongoDB. It includes two functions: serializeDict, which 
converts MongoDB documents to dictionaries with appropriate type handling for 
object IDs and datetime objects.
serializeList, which applies this serialization to a list of documents.
"""


# Serialize data betweeen API Service and MongoDB
# Serialize MongoDB documents
def serializeDict(item) -> dict:
    return {
        # Converting _id to string
        i: str(item[i]) if i == '_id' else

        # Converting datetime objects to their ISO format
        item[i].isoformat() if isinstance(item[i], datetime) else

        # Leaving other types as they are
        item[i]
        for i in item
    }

# Serialize list of documents
def serializeList(items) -> list:
	return [serializeDict(item) for item in items]