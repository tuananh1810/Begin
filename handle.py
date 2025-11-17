def Paginate(data, query_params, page=1, limit=100):
    page = int(query_params.get("page", page))
    limit = int(query_params.get("limit", limit))
    start = (page - 1) * limit
    end = page * limit
    return data[start:end]
