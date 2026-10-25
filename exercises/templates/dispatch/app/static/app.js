async function request(path, body) {
  const response = await fetch(path, body === undefined ? {} : {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)});
  const data = await response.json();
  if (!response.ok) throw new Error(`${response.status}: ${JSON.stringify(data.detail)}`);
  return data;
}
function show(id, value) { document.getElementById(id).textContent = JSON.stringify(value, null, 2); }
async function refresh() { for (const name of ['inventory', 'orders', 'rates', 'events']) show(name, await request(`/api/${name}`)); }
function bind(id, action) {
  document.getElementById(id).addEventListener('submit', async event => {
    event.preventDefault();
    try { show('result', await action(new FormData(event.target))); await refresh(); }
    catch (error) { show('result', error.message); }
  });
}
bind('quote', form => request('/api/quotes', {weights_grams: form.get('weights').split(',').map(Number), service: form.get('service'), signature: form.get('signature') === 'true'}));
bind('order', form => request('/api/orders', {customer: form.get('customer'), items: [{sku: form.get('sku'), quantity: Number(form.get('quantity'))}]}));
bind('ship', form => request('/api/shipments', {order_id: form.get('order_id'), service: form.get('service')}));
bind('cancel', form => request(`/api/orders/${encodeURIComponent(form.get('order_id'))}/cancel`, {}));
document.getElementById('refresh').onclick = () => refresh().catch(error => show('result', error.message));
refresh().catch(error => show('result', error.message));
