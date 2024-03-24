from datetime import datetime

# Serialize data betweeen API Service and MongoDB
# Serialize Dictionary
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

# Serialize list of Dictionaries
def serializeList(items) -> list:
	return [serializeDict(item) for item in items]