async function request(path, body) {
  const response = await fetch(path, body === undefined ? {} : {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)});
  const data = await response.json();
  if (!response.ok) throw new Error(`${response.status}: ${JSON.stringify(data.detail)}`);
  return data;
}
function show(id, value) { document.getElementById(id).textContent = JSON.stringify(value, null, 2); }
async function refresh() {
  for (const name of ['overview', 'agents', 'events']) show(name, await request(`/api/${name}`));
}
function bind(id, action) {
  document.getElementById(id).addEventListener('submit', async event => {
    event.preventDefault();
    try { await action(new FormData(event.target)); await refresh(); }
    catch (error) { show('result', error.message); }
  });
}
bind('queue', async form => show('queue-output', await request(`/api/queues?${new URLSearchParams(form)}`)));
bind('assign', async form => show('result', await request('/api/assignments', {ticket_ids: form.get('tickets').split(',').map(s => s.trim()), agent_id: form.get('agent'), actor: 'learner'})));
bind('comment', async form => show('result', await request(`/api/tickets/${encodeURIComponent(form.get('ticket'))}/comments`, {body: form.get('body'), actor: 'learner'})));
bind('status', async form => show('result', await request(`/api/tickets/${encodeURIComponent(form.get('ticket'))}/status`, {status: form.get('status'), actor: 'learner'})));
document.getElementById('refresh').onclick = () => refresh().catch(error => show('result', error.message));
refresh().catch(error => show('result', error.message));
