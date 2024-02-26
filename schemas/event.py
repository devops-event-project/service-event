from datetime import datetime

# def serializeDict(item) -> dict:
# 	return {**{i:str(item[i]) for i in item if i=='_id'},**{i:item[i] for i in item if i!='_id'}}

def serializeDict(item) -> dict:
    return {
        # Convert _id to string
        i: str(item[i]) if i == '_id' else

        # Convert datetime objects to their ISO format
        item[i].isoformat() if isinstance(item[i], datetime) else

        # Leave other types as they are
        item[i]
        for i in item
    }

def serializeList(items) -> list:
	return [serializeDict(item) for item in items]