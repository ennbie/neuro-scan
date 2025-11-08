document.getElementById("predict-btn").addEventListener("click", async () => {
  const fileInput = document.getElementById("file-input");
  const result = document.getElementById("result");
  const bar = document.getElementById("confidence-bar");

  if (!fileInput.files.length) {
    alert("Please select an image first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  result.innerText = "Processing...";
  bar.style.width = "0%";
  bar.innerText = "0%";

  const res = await fetch("/predict", { method: "POST", body: formData });
  const data = await res.json();

  result.innerText = `Prediction: ${data.prediction} (Confidence: ${data.confidence}%)`;

  bar.style.width = `${data.confidence}%`;
  bar.innerText = `${data.confidence}%`;
  bar.classList.remove("bg-success", "bg-warning", "bg-danger");

  if (data.confidence >= 80) bar.classList.add("bg-success");
  else if (data.confidence >= 60) bar.classList.add("bg-warning");
  else bar.classList.add("bg-danger");
});
