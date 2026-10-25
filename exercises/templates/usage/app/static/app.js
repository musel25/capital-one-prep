async function request(path, body) {
  const response = await fetch(path, body === undefined ? {} : {
    method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)
  });
  const data = await response.json();
  if (!response.ok) throw new Error(`${response.status}: ${JSON.stringify(data.detail)}`);
  return data;
}
function show(id, data) { document.getElementById(id).textContent = JSON.stringify(data, null, 2); }
function report(error) { document.getElementById('message').textContent = error.message; }

async function invoice() {
  const data = Object.fromEntries(new FormData(document.getElementById('invoice')));
  show('bill', await request(`/api/workspaces/${encodeURIComponent(data.workspace_id)}/bill?month=${encodeURIComponent(data.month)}`));
}
async function refresh() {
  show('events', (await request('/api/events')).items);
  await invoice();
}
document.getElementById('invoice').addEventListener('submit', async event => {
  event.preventDefault(); try { await invoice(); } catch (error) { report(error); }
});
document.getElementById('ingest').addEventListener('submit', async event => {
  event.preventDefault();
  const body = Object.fromEntries(new FormData(event.target));
  body.units = Number(body.units);
  try {
    const result = await request('/api/events', body);
    document.getElementById('message').textContent = `Recorded ${result.event_id}`;
    await refresh();
  } catch (error) { report(error); }
});
refresh().catch(report);
