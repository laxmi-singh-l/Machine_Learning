const form = document.getElementById("predictForm");
const resultDiv = document.getElementById("result");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(form);

  const payload = {
    age: Number(formData.get("age")),
    weight: Number(formData.get("weight")),
    height: Number(formData.get("height")),
    income_lpa: Number(formData.get("income_lpa")),
    smoker: formData.get("smoker") === "true",
    city: formData.get("city"),
    occupation: formData.get("occupation")
  };

  try {
    const res = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (!res.ok) {
      resultDiv.innerText = "Error: " + JSON.stringify(data);
      return;
    }

    resultDiv.innerText = "Predicted Category: " + data.predicted_category;

  } catch (err) {
    resultDiv.innerText = "Server not reachable";
  }
});
