async function loadCurrencies() {
  const res = await fetch("/rates");
  const currencies = await res.json();

  const from = document.getElementById("from");
  const to = document.getElementById("to");

  currencies.forEach(c => {
    from.add(new Option(c, c));
    to.add(new Option(c, c));
  });

  from.value = "USD";
  to.value = "BRL";
}

async function convert() {
  const amount = document.getElementById("amount").value;
  const from = document.getElementById("from").value;
  const to = document.getElementById("to").value;

  const res = await fetch(`/convert?amount=${amount}&from=${from}&to=${to}`);
  const data = await res.json();

  document.getElementById("result").innerText =
    `${data.result} ${data.to}`;
}

loadCurrencies();