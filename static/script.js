async function sendMessage() {
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    const userText = input.value.trim();
    if (!userText) return;

    chatBox.innerHTML += `<div class="message user"><b>You:</b> ${userText}</div>`;
    input.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    const response = await fetch("/generate", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({prompt: userText})
    });

    const data = await response.json();
    const botText = data.response || "Error generating response.";

    chatBox.innerHTML += `<div class="message bot"><b>MedBot:</b> ${botText}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}
