const backendURL = "https://code-generator-x3de.onrender.com/generate";

async function generateCode() {
  const prompt = document.getElementById("prompt").value.trim();
  const output = document.getElementById("output");
  const error = document.getElementById("error");
  const loader = document.getElementById("loader");

  output.textContent = "";
  error.textContent = "";

  if (!prompt) {
    error.textContent = "⚠️ Prompt cannot be empty.";
    return;
  }

  loader.style.display = "block";

  try {
    const response = await fetch(backendURL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ prompt: prompt })
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.error || "Something went wrong with the backend.");
    }

    const data = await response.json();
    output.textContent = data.code || "⚠️ No output received from model.";
  } catch (err) {
    error.textContent = `❌ ${err.message}`;
  } finally {
    loader.style.display = "none";
  }
}
