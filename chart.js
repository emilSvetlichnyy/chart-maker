const COLORS = [
  "#0f7a6c",
  "#d9773a",
  "#2f5d8c",
  "#b44d6a",
  "#6b8f3a",
  "#7a5caf",
];

function parseRows(container) {
  return [...container.querySelectorAll(".row")].map((row) => {
    const label = row.querySelector('[data-field="label"]').value.trim();
    const value = Number(row.querySelector('[data-field="value"]').value);
    return {
      label: label || "Без названия",
      value: Number.isFinite(value) ? Math.max(0, value) : 0,
    };
  }).filter((item) => item.value > 0);
}

function drawPie(canvas, data) {
  const ctx = canvas.getContext("2d");
  const dpr = window.devicePixelRatio || 1;
  const size = 280;
  canvas.width = size * dpr;
  canvas.height = size * dpr;
  canvas.style.width = `${size}px`;
  canvas.style.height = `${size}px`;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, size, size);

  const total = data.reduce((sum, item) => sum + item.value, 0);
  if (!total) {
    ctx.fillStyle = "#6b7c88";
    ctx.font = "15px Figtree, sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("Добавьте числа", size / 2, size / 2);
    return [];
  }

  const cx = size / 2;
  const cy = size / 2;
  const radius = 108;
  const inner = 58;
  let angle = -Math.PI / 2;
  const legend = [];

  data.forEach((item, index) => {
    const slice = (item.value / total) * Math.PI * 2;
    const color = COLORS[index % COLORS.length];
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.arc(cx, cy, radius, angle, angle + slice);
    ctx.closePath();
    ctx.fillStyle = color;
    ctx.fill();
    legend.push({
      ...item,
      color,
      pct: Math.round((item.value / total) * 100),
    });
    angle += slice;
  });

  ctx.beginPath();
  ctx.fillStyle = "#fbfcfb";
  ctx.arc(cx, cy, inner, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#152028";
  ctx.font = "700 22px Syne, sans-serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(String(total), cx, cy - 8);
  ctx.fillStyle = "#6b7c88";
  ctx.font = "12px Figtree, sans-serif";
  ctx.fillText("сумма", cx, cy + 12);

  return legend;
}

function drawBar(canvas, data) {
  const ctx = canvas.getContext("2d");
  const dpr = window.devicePixelRatio || 1;
  const width = 320;
  const height = 260;
  canvas.width = width * dpr;
  canvas.height = height * dpr;
  canvas.style.width = `${width}px`;
  canvas.style.height = `${height}px`;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, width, height);

  if (!data.length) {
    ctx.fillStyle = "#6b7c88";
    ctx.font = "15px Figtree, sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("Добавьте числа", width / 2, height / 2);
    return [];
  }

  const max = Math.max(...data.map((item) => item.value));
  const pad = { top: 16, right: 12, bottom: 48, left: 12 };
  const plotW = width - pad.left - pad.right;
  const plotH = height - pad.top - pad.bottom;
  const gap = 10;
  const barW = (plotW - gap * (data.length - 1)) / data.length;
  const legend = [];

  data.forEach((item, index) => {
    const color = COLORS[index % COLORS.length];
    const h = max ? (item.value / max) * plotH : 0;
    const x = pad.left + index * (barW + gap);
    const y = pad.top + plotH - h;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.roundRect(x, y, barW, h, [8, 8, 2, 2]);
    ctx.fill();

    ctx.fillStyle = "#3d4f5c";
    ctx.font = "11px Figtree, sans-serif";
    ctx.textAlign = "center";
    const label = item.label.length > 10 ? `${item.label.slice(0, 9)}…` : item.label;
    ctx.fillText(label, x + barW / 2, height - 28);
    ctx.fillStyle = "#152028";
    ctx.font = "650 12px Figtree, sans-serif";
    ctx.fillText(String(item.value), x + barW / 2, y - 6);

    legend.push({
      ...item,
      color,
      pct: Math.round((item.value / data.reduce((s, i) => s + i.value, 0)) * 100),
    });
  });

  return legend;
}

function renderLegend(table, legend) {
  const body = legend
    .map(
      (item) => `
      <tr>
        <td><span class="swatch" style="background:${item.color}"></span>${item.label}</td>
        <td>${item.value}</td>
        <td>${item.pct}%</td>
      </tr>`
    )
    .join("");
  table.querySelector("tbody").innerHTML = body || "";
}

function downloadCanvas(canvas, name) {
  const link = document.createElement("a");
  link.download = name;
  link.href = canvas.toDataURL("image/png");
  link.click();
}

function bindTool({ type, rowsId, canvasId, legendId, addBtnId, downloadBtnId, totalId }) {
  const rows = document.getElementById(rowsId);
  const canvas = document.getElementById(canvasId);
  const legend = document.getElementById(legendId);
  const addBtn = document.getElementById(addBtnId);
  const downloadBtn = document.getElementById(downloadBtnId);
  const totalEl = document.getElementById(totalId);

  function rowTemplate(label = "", value = "") {
    const el = document.createElement("div");
    el.className = "row";
    el.innerHTML = `
      <label>Название
        <input data-field="label" type="text" value="${label}" placeholder="Сектор">
      </label>
      <label>Значение
        <input data-field="value" type="number" min="0" step="any" value="${value}" placeholder="0">
      </label>
      <button type="button" class="btn btn-ghost" data-remove>Удалить</button>
    `;
    return el;
  }

  function refresh() {
    const data = parseRows(rows);
    const drawn = type === "bar" ? drawBar(canvas, data) : drawPie(canvas, data);
    renderLegend(legend, drawn);
    const total = data.reduce((sum, item) => sum + item.value, 0);
    if (totalEl) totalEl.textContent = `Сумма: ${total}`;
    [...rows.querySelectorAll("[data-remove]")].forEach((btn) => {
      btn.disabled = rows.querySelectorAll(".row").length <= 2;
    });
  }

  rows.addEventListener("input", refresh);
  rows.addEventListener("click", (event) => {
    const btn = event.target.closest("[data-remove]");
    if (!btn) return;
    if (rows.querySelectorAll(".row").length <= 2) return;
    btn.closest(".row").remove();
    refresh();
  });

  addBtn?.addEventListener("click", () => {
    if (rows.querySelectorAll(".row").length >= 8) return;
    rows.appendChild(rowTemplate(`Сектор ${rows.querySelectorAll(".row").length + 1}`, "10"));
    refresh();
  });

  downloadBtn?.addEventListener("click", () => {
    downloadCanvas(canvas, type === "bar" ? "bar-chart.png" : "pie-chart.png");
  });

  refresh();
}

window.ChartMaker = { bindTool };
