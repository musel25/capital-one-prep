async function refresh() {
  for (const id of ['products', 'reservations']) document.getElementById(id).textContent = JSON.stringify(await (await fetch(`/api/${id}`)).json(), null, 2);
}
document.getElementById('reserve').addEventListener('submit', async (event) => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const response = await fetch('/api/reservations', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ items: [{ sku: form.get('sku'), quantity: Number(form.get('quantity')) }] }) });
  document.getElementById('message').textContent = JSON.stringify(await response.json());
  await refresh();
});
document.getElementById('cancel').addEventListener('submit', async (event) => {
  event.preventDefault();
  const id = new FormData(event.currentTarget).get('id');
  const response = await fetch(`/api/reservations/${encodeURIComponent(id)}/cancel`, { method: 'POST' });
  document.getElementById('message').textContent = JSON.stringify(await response.json());
  await refresh();
});
refresh();
