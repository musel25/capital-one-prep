from .representation import invoice


def bill(feed, workspace_id, month):
    feed.require_workspace(workspace_id)
    rows = [row for row in feed.events if row['workspace_id'] == workspace_id
            and row['month'] == month and row['status'] == 'accepted']
    samples = {(row['meter_id'], row['sample_id']): row for row in rows}
    units = sum(row['units'] for row in samples.values())
    return invoice(workspace_id, month, len(samples), units)
