async function refresh() {
  for (const name of ['equipment', 'loans']) {
    const response = await fetch(`/api/${name}`);
    document.getElementById(name).textContent = JSON.stringify(await response.json(), null, 2);
  }
}
async function perform(url, body) {
  try {
    const response = await fetch(url, {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      ...(body ? {body: JSON.stringify(body)} : {}),
    });
    document.getElementById('result').textContent = `${response.status}\n${JSON.stringify(await response.json(), null, 2)}`;
    await refresh();
  } catch (error) { document.getElementById('result').textContent = error.message; }
}
document.getElementById('checkout').addEventListener('submit', (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(event.currentTarget));
  data.quantity = Number(data.quantity);
  perform('/api/loans', data);
});
document.getElementById('return').addEventListener('submit', (event) => {
  event.preventDefault();
  const id = new FormData(event.currentTarget).get('loan_id');
  perform(`/api/loans/${encodeURIComponent(id)}/return`);
});
refresh().catch((error) => { document.getElementById('result').textContent = error.message; });
