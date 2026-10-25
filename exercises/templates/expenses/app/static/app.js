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

async function refresh() { show('expenses', (await request('/api/expenses')).items); }
document.getElementById('summary').addEventListener('submit', async event => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(event.target));
  try { show('totals', await request(`/api/employees/${encodeURIComponent(data.employee_id)}/summary?month=${encodeURIComponent(data.month)}`)); }
  catch (error) { report(error); }
});
document.getElementById('claim').addEventListener('submit', async event => {
  event.preventDefault();
  const body = Object.fromEntries(new FormData(event.target));
  body.amount_cents = Number(body.amount_cents);
  try {
    const result = await request('/api/expenses', body);
    document.getElementById('message').textContent = `Submitted ${result.id}; awaiting review.`;
    await refresh();
    document.getElementById('totals').textContent = 'Ledger changed. Request the summary again to refresh totals.';
  } catch (error) { report(error); }
});
refresh().catch(report);
