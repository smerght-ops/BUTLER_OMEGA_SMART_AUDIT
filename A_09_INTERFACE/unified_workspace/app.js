const panelOrder = ["conversation", "voice", "tasks", "council", "models", "memory", "skills", "files", "permissions", "logs", "results"];
const title = key => key.replaceAll("_", " ").replace(/\b\w/g, c => c.toUpperCase());
const compact = value => JSON.stringify(value, null, 2);

function render(data) {
  const taskStats = data.runtime.tasks;
  document.querySelector("#health").textContent = "Runtime online";
  document.querySelector("#health").classList.add("online");
  document.querySelector("#summary").innerHTML = [
    ["Tasks", taskStats.total], ["Running", taskStats.running], ["Completed", taskStats.completed], ["Failed", taskStats.failed]
  ].map(([label, value]) => `<article><strong>${value}</strong><span>${label}</span></article>`).join("");
  document.querySelector("#panels").innerHTML = panelOrder.map(key => `
    <article class="panel"><div class="panel-title"><h3>${title(key)}</h3><span>READ ONLY</span></div><pre>${compact(data[key])}</pre></article>
  `).join("");
}

async function refresh() {
  try {
    const response = await fetch("/api/dashboard", {cache: "no-store"});
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    render(await response.json());
  } catch (error) {
    document.querySelector("#health").textContent = "Runtime unavailable";
    document.querySelector("#panels").innerHTML = `<article class="panel error"><h3>Connection error</h3><p>${error.message}</p></article>`;
  }
}

refresh();
setInterval(refresh, 5000);
