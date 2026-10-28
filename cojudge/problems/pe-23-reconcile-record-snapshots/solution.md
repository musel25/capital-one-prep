## Reference solution

```python
def reconcile_records(local, remote):
    local_by_id = {record["id"]: record for record in local}
    remote_by_id = {record["id"]: record for record in remote}
    result = {"upload": [], "download": [], "conflicts": []}
    for record_id in sorted(local_by_id.keys() | remote_by_id.keys()):
        if record_id not in remote_by_id:
            result["upload"].append(record_id)
        elif record_id not in local_by_id:
            result["download"].append(record_id)
        else:
            left, right = local_by_id[record_id], remote_by_id[record_id]
            if left["version"] > right["version"]:
                result["upload"].append(record_id)
            elif left["version"] < right["version"]:
                result["download"].append(record_id)
            elif left["checksum"] != right["checksum"]:
                result["conflicts"].append(record_id)
    return result
```
