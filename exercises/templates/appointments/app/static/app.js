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

async function refresh() {
  show('providers', (await request('/api/providers')).items);
  show('bookings', (await request('/api/bookings')).items);
}
async function availability() {
  const query = new URLSearchParams(new FormData(document.getElementById('availability')));
  show('slots', await request(`/api/availability?${query}`));
}
document.getElementById('availability').addEventListener('submit', async event => {
  event.preventDefault();
  try { await availability(); document.getElementById('message').textContent = ''; }
  catch (error) { report(error); }
});
document.getElementById('booking').addEventListener('submit', async event => {
  event.preventDefault();
  const body = Object.fromEntries(new FormData(event.target));
  body.duration_minutes = Number(body.duration_minutes);
  try {
    const result = await request('/api/bookings', body);
    document.getElementById('message').textContent = `Booked ${result.id}: ${result.start}–${result.end}`;
    await refresh();
    document.getElementById('slots').textContent = 'Bookings changed. Find appointments again to refresh availability.';
  } catch (error) { report(error); }
});
refresh().catch(report);
