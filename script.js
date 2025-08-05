
const canvas = document.getElementById("simCanvas");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = 400;

function prime(n) {
  let count = 0, num = 2;
  while (true) {
    if ([...Array(num).keys()].slice(2).every(i => num % i !== 0)) {
      count++;
      if (count === n) return num;
    }
    num++;
  }
}

function primeHarmonic(t, sigma_h = 0.99) {
  let sum = 0;
  for (let k = 1; k <= 60; k++) {
    sum += prime(k) * Math.sin(2 * Math.PI * sigma_h * k * t);
  }
  return sum;
}

let t = 0;
function animate() {
  ctx.fillStyle = "black";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.beginPath();
  ctx.strokeStyle = "lime";
  ctx.lineWidth = 2;
  ctx.moveTo(0, canvas.height / 2);

  for (let x = 0; x < canvas.width; x++) {
    const y = canvas.height / 2 - primeHarmonic(t + x * 0.001) * 0.5;
    ctx.lineTo(x, y);
  }

  ctx.stroke();
  t += 0.01;
  requestAnimationFrame(animate);
}
animate();

document.getElementById("donateButton").addEventListener("click", () => {
  alert("Silent Support Activated 🙏 — Thank you, Dr. Quantum salutes you.");
});
