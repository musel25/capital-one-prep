const $ = (id) => document.getElementById(id);
async function refresh() {
  const response = await fetch('/api/accounts');
  const { items } = await response.json();
  $('accounts').replaceChildren(...items.map((account) => {
    const li = document.createElement('li');
    li.textContent = `${account.id}: $${(account.balance_cents / 100).toFixed(2)}`;
    return li;
  }));
  const query = new URLSearchParams(new FormData($('filters')));
  if (!query.get('category')) query.delete('category');
  $('transactions').textContent = JSON.stringify(await (await fetch(`/api/transactions?${query}`)).json(), null, 2);
}
$('filters').addEventListener('submit', (event) => { event.preventDefault(); refresh().catch(showError); });
$('transfer').addEventListener('submit', async (event) => {
  event.preventDefault();
  try {
    const form = new FormData(event.currentTarget);
    const response = await fetch('/api/transfers', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ source: form.get('source'), target: form.get('target'), amount_cents: Number(form.get('amount')) }) });
    const result = await response.json();
    $('message').textContent = response.ok ? `Transfer ${result.id} recorded.` : JSON.stringify(result.detail);
    await refresh();
  } catch (error) { showError(error); }
});
function showError(error) { $('message').textContent = String(error); }
refresh().catch(showError);
