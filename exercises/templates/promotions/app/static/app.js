const form = document.getElementById('purchase');
async function refresh() {
  const data = new FormData(form);
  const body = JSON.stringify({ at: data.get('at'), amount_cents: Number(data.get('amount_cents')), active_member: data.has('active_member') });
  for (const [id, url] of [['eligibility', '/api/eligibility'], ['quote', '/api/rewards/quote']]) {
    const response = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body });
    document.getElementById(id).textContent = JSON.stringify(await response.json(), null, 2);
  }
}
form.addEventListener('submit', (event) => { event.preventDefault(); refresh(); });
refresh();
