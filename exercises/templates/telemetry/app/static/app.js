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

function latencyLabel(reading) { return `${reading.duration_ms.toFixed(1)} ms`; }
async function refresh() {
  const service = new FormData(document.getElementById('service')).get('service_id');
  const path = `/api/services/${encodeURIComponent(service)}`;
  show('overview', await request(`${path}/summary`));
  const rows = (await request(`${path}/readings`)).items;
  const list = document.getElementById('readings');
  list.replaceChildren(...rows.map(row => {
    const item = document.createElement('li');
    item.textContent = `${row.id}: ${latencyLabel(row)} · ${row.status}`;
    return item;
  }));
}
document.getElementById('service').addEventListener('submit', async event => {
  event.preventDefault(); try { await refresh(); } catch (error) { report(error); }
});
document.getElementById('collect').addEventListener('submit', async event => {
  event.preventDefault();
  const body = Object.fromEntries(new FormData(event.target));
  body.duration_us = Number(body.duration_us);
  try {
    const result = await request('/api/readings', body);
    document.getElementById('message').textContent = `Collected ${result.id}: ${latencyLabel(result)}`;
    await refresh();
  } catch (error) { report(error); }
});
refresh().catch(report);
