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

async function refresh() { show('contacts', (await request('/api/contacts')).items); }
document.getElementById('contact').addEventListener('submit', async event => {
  event.preventDefault();
  try {
    const result = await request('/api/contacts', Object.fromEntries(new FormData(event.target)));
    document.getElementById('message').textContent = `Added ${result.name}`;
    await refresh();
  } catch (error) { report(error); }
});
document.getElementById('import').addEventListener('submit', async event => {
  event.preventDefault();
  try {
    const contacts = JSON.parse(new FormData(event.target).get('contacts'));
    const result = await request('/api/imports', {contacts});
    document.getElementById('message').textContent = `Imported ${result.items.length} contacts`;
    await refresh();
  } catch (error) { report(error); }
});
refresh().catch(report);
