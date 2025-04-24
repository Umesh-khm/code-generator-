async function generateCode() {
  const prompt = document.getElementById("prompt").value;
  const output = document.getElementById("output");

  output.textContent = "⏳ Generating code...";

  try {
    const res = await fetch("https://code-generator-x3de.onrender.com", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ prompt: prompt })
    });

    const data = await res.json();

    if (data.error) {
      output.textContent = "❌ Error: " + data.error;
    } else {
      output.textContent = data.code;
    }

  } catch (err) {
    output.textContent = "❌ Error: " + err.message;
  }
}
