let products = [];
const message = document.querySelector('#message');
const money = cents => `$${(cents / 100).toFixed(2)}`;
async function api(path, body) {
  const response = await fetch(path, body ? {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)} : {});
  const data = await response.json();
  if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'Please check quantities and discount.');
  return data;
}
function addLine() {
  const row = document.createElement('fieldset');
  const legend = document.createElement('legend'); legend.textContent = 'Invoice line';
  const select = document.createElement('select'); select.name = 'sku'; select.setAttribute('aria-label', 'Product');
  products.forEach(product => select.add(new Option(product.name, product.sku)));
  const quantity = document.createElement('input');
  Object.assign(quantity, {name: 'quantity', type: 'number', min: '1', max: '100', step: '1', value: '1', required: true});
  quantity.setAttribute('aria-label', 'Quantity');
  const remove = document.createElement('button'); remove.type = 'button'; remove.textContent = 'Remove line';
  remove.addEventListener('click', () => row.remove());
  row.append(legend, select, quantity, remove); document.querySelector('#lines').append(row);
}
document.querySelector('#add-line').addEventListener('click', addLine);
document.querySelector('#invoice-form').addEventListener('submit', async event => {
  event.preventDefault();
  const lines = [...document.querySelectorAll('#lines fieldset')].map(row => ({sku: row.querySelector('select').value, quantity: Number(row.querySelector('input').value)}));
  try {
    const result = await api('/api/invoices/preview', {lines, discount_percent: Number(event.target.elements.discount.value)});
    const table = document.querySelector('#preview-lines'); table.replaceChildren();
    for (const item of result.lines) {
      const row = document.createElement('tr');
      for (const value of [item.sku, item.quantity, money(item.subtotal_cents), money(item.discount_cents), money(item.total_cents)]) {
        const cell = document.createElement('td'); cell.textContent = value; row.append(cell);
      }
      table.append(row);
    }
    document.querySelector('#totals').textContent = `Subtotal ${money(result.subtotal_cents)} · Discount ${money(result.discount_cents)} · Total ${money(result.total_cents)}`;
    message.textContent = 'Preview calculated.';
  } catch (error) { message.textContent = error.message; }
});
async function start() {
  try {
    products = (await api('/api/products')).items;
    for (const product of products) {
      const item = document.createElement('li'); item.textContent = `${product.name}: ${money(product.unit_cents)} each`;
      document.querySelector('#catalog').append(item);
    }
    addLine();
  } catch (error) { message.textContent = error.message; }
}
start();
