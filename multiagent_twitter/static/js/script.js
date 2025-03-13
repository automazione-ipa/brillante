document.getElementById("createPostForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const topic = document.getElementById("topic").value;

    fetch("/create_post", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ topic: topic })
    })
    .then(response => response.json())
    .then(data => {
        const message = data.message || data.error;
        document.getElementById("response").textContent = message;
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
