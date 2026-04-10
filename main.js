const data = {
  week: "Week ending 2026-04-10",
  performance: {
    current: { sales: 41750, conversion: 3.1, reviews: 4.2, returns: 2.8, stockRisk: "2 days", priceChange: "-3.4%", accountHealth: 87 },
    previous: { sales: 48200, conversion: 3.4, reviews: 4.3, returns: 2.4, stockRisk: "1 day", priceChange: "+0.8%", accountHealth: 92 }
  },
  brandHealth: [
    ["Sales", "$41.8k", "vs $48.2k last week", "down 13.4%"],
    ["Conversion", "3.1%", "vs 3.4% last week", "down 0.3pp"],
    ["Reviews", "4.2 / 5", "vs 4.3 last week", "slight drift"],
    ["Stock risk", "2 days", "vs 1 day last week", "needs follow-up"],
    ["Price changes", "-3.4%", "vs +0.8% last week", "promo active"],
    ["Account health", "87", "vs 92 last week", "watch"]
  ],
  listingIssues: [
    "SKU-1001: weak title, short bullets, 5 images, keyword gap",
    "SKU-2044: compliance risk before any edits",
    "SKU-8820: bullet coverage below target, attributes need cleanup"
  ],
  reviewThemes: [
    ["quality", 3],
    ["delivery", 2],
    ["fit / sizing", 2],
    ["instructions", 1],
    ["defects", 1],
    ["praise", 2]
  ],
  competitors: [
    ["Competitor A", "$22.49", "4.4", "2.5k", "lower price + better ratings"],
    ["Competitor B", "$26.99", "4.1", "990", "premium price, weaker demand"],
    ["Competitor C", "$23.99", "4.6", "3.2k", "strong review momentum"]
  ],
  summary: {
    changed:
      "Sales fell, conversion softened, stock risk increased, and one listing is carrying compliance risk.",
    matters:
      "Performance pressure and stockouts are the biggest immediate risks. Competitors are outperforming on rating and price in spots.",
    next:
      "Check replenishment, fix the weakest listings, review pricing, and escalate the compliance item before publishing changes."
  }
};

const money = (value) => `$${value}`;

const $ = (id) => document.getElementById(id);
const modules = Array.from(document.querySelectorAll(".module"));
const filterButtons = Array.from(document.querySelectorAll(".filter-pill"));
const searchInput = $("moduleSearch");

$("salesMetric").textContent = money(data.performance.current.sales / 1000).replace(".0", "");
$("conversionMetric").textContent = `${data.performance.current.conversion}%`;
$("healthMetric").textContent = `${data.performance.current.accountHealth}`;

$("signalList").innerHTML = [
  { label: "Sales delta", value: "-13.4% vs last week" },
  { label: "Stock risk", value: data.performance.current.stockRisk },
  { label: "Compliance", value: "1 item flagged" }
]
  .map(
    (item) => `
      <div class="signal">
        <strong>${item.label}</strong>
        <span>${item.value}</span>
      </div>`
  )
  .join("");

$("brandHealthTable").innerHTML = data.brandHealth
  .map(
    ([metric, value, context, signal]) => `
      <div class="table-row">
        <div>
          <strong>${metric}</strong>
          <small>${context}</small>
        </div>
        <div>${value}</div>
        <div>${signal}</div>
        <div><span>AI flags it, human decides what to do.</span></div>
      </div>`
  )
  .join("");

$("listingIssues").innerHTML = data.listingIssues.map((issue) => `<li>${issue}</li>`).join("");

$("reviewThemes").innerHTML = data.reviewThemes
  .map(([theme, count]) => `<span class="chip">${theme} <strong>${count}</strong></span>`)
  .join("");

$("competitorList").innerHTML = data.competitors
  .map(
    ([name, price, rating, reviews, note]) => `
      <div class="competitor-row">
        <div>
          <strong>${name}</strong>
          <span>${note}</span>
        </div>
        <div>${price}</div>
        <div>${rating}</div>
        <div>${reviews}</div>
      </div>`
  )
  .join("");

$("whatChanged").textContent = data.summary.changed;
$("whatMatters").textContent = data.summary.matters;
$("whatNext").textContent = data.summary.next;

const chartCtx = $("healthChart");
if (chartCtx && window.Chart) {
  new Chart(chartCtx, {
    type: "line",
    data: {
      labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
      datasets: [
        {
          label: "Sales",
          data: [46.2, 45.4, 44.8, 43.1, 42.8, 42.0, 41.75],
          borderColor: "#1d4ed8",
          backgroundColor: "rgba(29, 78, 216, 0.08)",
          tension: 0.35,
          pointRadius: 2,
          fill: true
        },
        {
          label: "Conversion",
          data: [3.5, 3.4, 3.3, 3.2, 3.1, 3.1, 3.1],
          borderColor: "#146c43",
          backgroundColor: "rgba(20, 108, 67, 0.08)",
          tension: 0.35,
          pointRadius: 2,
          fill: false
        },
        {
          label: "Account health",
          data: [92, 91, 90, 89, 88, 87, 87],
          borderColor: "#9a6700",
          backgroundColor: "rgba(154, 103, 0, 0.08)",
          tension: 0.35,
          pointRadius: 2,
          fill: false
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#101010",
          titleColor: "#fff",
          bodyColor: "#fff"
        }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: "#5d5a53" } },
        y: { grid: { color: "rgba(16,16,16,0.08)" }, ticks: { color: "#5d5a53" } }
      }
    }
  });
}

function applyFilters() {
  const activeFilter = document.querySelector(".filter-pill.active")?.dataset.filter ?? "all";
  const term = searchInput.value.trim().toLowerCase();

  modules.forEach((module) => {
    const tags = (module.dataset.tags || "").toLowerCase();
    const text = module.textContent.toLowerCase();
    const matchesFilter = activeFilter === "all" || tags.includes(activeFilter);
    const matchesTerm = !term || text.includes(term);
    module.classList.toggle("is-hidden", !(matchesFilter && matchesTerm));
  });
}

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    filterButtons.forEach((btn) => btn.classList.remove("active"));
    button.classList.add("active");
    applyFilters();
  });
});

searchInput.addEventListener("input", applyFilters);
