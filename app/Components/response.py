def Response(status: int, message=None, data=None):
    return {
        "status": status,
        "message": message,
        "data": data
    }, status